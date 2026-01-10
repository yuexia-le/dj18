# app.py
from flask import Flask, render_template, request, jsonify
from config import Config
from models import db, Word
from services import get_translation, generate_story, generate_sentence_challenge
import os
import re # 引入正则表达式库

# 定义一个正则表达式来匹配大部分中文字符
CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]')

# 引入一个简单的全局缓存，存储最近的句子挑战，用于避免重复
RECENT_SENTENCE_CHALLENGES = []
MAX_CACHE_SIZE = 5


app = Flask(__name__)
app.config.from_object(Config)
# --- 增加 SQLAlchemy 连接池配置 ---
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    # 启用连接回收机制，每 300 秒 (5 分钟) 检查一次连接是否超时
    "pool_recycle": 300, 
    # 连接池大小，根据你的需求调整
    "pool_size": 10,
    # 连接超时时间 (如果连接超过 10 秒没获取到就报错)
    "pool_timeout": 10 
}
db.init_app(app)

# 初始化数据库
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- API 接口 ---

@app.route('/api/words', methods=['GET'])
def get_words():
    words = Word.query.all()
    return jsonify([w.to_dict() for w in words])

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if file:
        content = file.read().decode('utf-8')
        lines = content.splitlines()
        count = 0
        new_words_list = [] 
        
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 默认设置为需要翻译
            eng = line # ⚠️ 初始值为整行，这是危险的
            cn = '待翻译...'
            needs_translation = True
            
            # 尝试将整行分割成词汇列表
            parts = line.split() 
            
            if not parts:
                continue
                
            # 默认为只有英文，取第一个词
            eng = parts[0].strip()
            
            # 1. 检查是否包含中文
            # 检查整个原始行是否包含中文，或者 parts 列表是否有超过一个元素（可能是英文+中文）
            if CHINESE_CHAR_PATTERN.search(line) or len(parts) > 1:
                
                # 如果是 "英文 翻译" 格式，且不是只有英文，则尝试取第二部分作为中文
                if len(parts) > 1:
                    # 将第一个词后面的所有内容作为中文翻译（用 maxsplit=1 更精确）
                    _, cn_raw = line.split(maxsplit=1) 
                    cn = cn_raw.strip()
                    needs_translation = False # 标记为不需要翻译
                else:
                    # 包含中文，但格式不正确 (如：只有 "苹果")，仍标记为待翻译
                    pass 
                    
            if eng and not Word.query.filter_by(english=eng).first():
                new_word = Word()
                new_word.english = eng 
                new_word.chinese = cn 
                db.session.add(new_word)
                db.session.flush()
                new_words_list.append(new_word.to_dict())
                count += 1
                
                if needs_translation:
                    pass
                
        db.session.commit()
        return jsonify({
            'message': f'成功导入 {count} 个新单词，正在后台排队翻译。',
            'new_words': new_words_list
        })
    return jsonify({'error': 'File error'}), 400

# --- 增加一个专门用于触发翻译的 API ---
@app.route('/api/translate_word/<int:word_id>', methods=['POST'])
def translate_word_api(word_id):
    word = Word.query.get(word_id)
    if not word or word.chinese != "待翻译...":
        return jsonify({'message': '单词已翻译或不存在'}), 200
        
    try:
        # 调用 AI 翻译
        cn = get_translation(word.english) 
        
        word.chinese = cn
        db.session.commit()
        return jsonify({'message': '翻译成功', 'chinese': cn}), 200
    except Exception as e:
        # 如果速率限制触发，返回特定的错误代码
        return jsonify({'error': '翻译失败，可能是速率限制', 'details': str(e)}), 500

@app.route('/api/words/<int:id>', methods=['DELETE'])
def delete_word(id):
    word = Word.query.get_or_404(id)
    db.session.delete(word)
    db.session.commit()
    return jsonify({'message': 'Deleted'}),200

@app.route('/api/story', methods=['POST'])
def get_story():
    # 获取随机 10 个单词生成故事
    words = Word.query.order_by(db.func.random()).limit(10).all()
    word_list = [w.english for w in words]
    if not word_list:
        return jsonify({'story': '词库为空，请先上传单词。'})
    story = generate_story(word_list)
    if story and isinstance(story, str):
        if "limit exceeded" in story.lower():
            return jsonify({'story': '操作太快啦！请 30 秒后再试。'}), 429
        return jsonify({'story': story})
    else:
        # 如果 story 是 None 或其他非字符串
        return jsonify({'story': 'AI 助手暂时掉线了，请稍后再试。'}), 500

@app.route('/api/sentence', methods=['GET'])
def get_sentence():
   # 传递缓存中的句子，要求AI避开它们
    recent_cn_sentences = [item['chinese'] for item in RECENT_SENTENCE_CHALLENGES]
    
    # 修改 generate_sentence_challenge 函数，让它接受一个排除列表
    data = generate_sentence_challenge(exclude_sentences=recent_cn_sentences)
    
    if data:
        # 更新缓存
        RECENT_SENTENCE_CHALLENGES.append(data)
        if len(RECENT_SENTENCE_CHALLENGES) > MAX_CACHE_SIZE:
            RECENT_SENTENCE_CHALLENGES.pop(0) # 移除最旧的句子
            
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

