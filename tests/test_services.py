import pytest
from services import get_translation, generate_story, generate_sentence_challenge
from config import Config
from unittest.mock import patch, MagicMock

def create_mock_response(content):
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message.content = content
    return mock_resp

# 测试翻译成功
@patch('services.client.chat.completions.create')
def test_get_translation_success(mock_create):
    mock_create.return_value = create_mock_response("苹果, 苹果树, 苹果派")
    result = get_translation("apple")
    assert result == "苹果, 苹果树, 苹果派"

# 测试翻译API异常
@patch('services.client.chat.completions.create')
def test_get_translation_api_exception(mock_create):
    mock_create.side_effect = Exception("API Error")
    result = get_translation("test")
    assert "翻译服务暂时不可用" in result

# 测试 API Key 缺失 (Mock Config)
def test_ai_key_missing():
    with patch('services.Config.SILICONFLOW_API_KEY', new=''):
        result = get_translation("test")
        assert "请配置 API KEY" in result

# 1. 测试 generate_story 的内部逻辑
@patch('services.client.chat.completions.create')
def test_generate_story_internal(mock_create):
    mock_create.return_value = create_mock_response("Once upon a time...")
    story = generate_story(["apple", "banana"])
    
    assert story is not None
    assert "Once upon a time" in str(story)

# 2. 测试 generate_sentence_challenge 的内部逻辑
@patch('services.client.chat.completions.create')
def test_generate_sentence_challenge_internal(mock_create):
    # 模拟 AI 返回了一个 JSON 字符串（这是最容易出错的地方！）
    mock_json = '{"chinese": "我吃苹果", "answer": "I eat apple"}'
    mock_create.return_value = create_mock_response(mock_json)
    
    result = generate_sentence_challenge(exclude_sentences=[])
    
    assert result['chinese'] == "我吃苹果"
    assert result['answer'] == "I eat apple"

# 3. 测试 AI 返回了非法的 JSON (鲁棒性测试)
@patch('services.client.chat.completions.create')
def test_generate_sentence_challenge_bad_json(mock_create):
    # 模拟 AI 没按要求返回 JSON，而是返回了普通句子
    mock_create.return_value = create_mock_response("这不是JSON格式")
    
    # 修复 TypeError：确保即使失败逻辑也跑过 join
    result = generate_sentence_challenge(exclude_sentences=["old sentence"])
    
    # 验证触发了 except 块
    assert "生成失败" in result['chinese']