import unittest
import re

# 只保留汉字的正则
CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def parse_line(line):
    line = line.strip()
    if not line:
        return {"eng": None, "cn": None, "needs_translation": None}

    eng = line
    cn = '待翻译'
    needs_translation = True

    if CHINESE_CHAR_PATTERN.search(line):
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            eng = parts[0].strip()
            cn = parts[1].strip()
            needs_translation = False

    return {"eng": eng, "cn": cn, "needs_translation": needs_translation}

# ----------------- 单元测试 -----------------
class TestParseLine(unittest.TestCase):
    def test_pure_english(self):
        res = parse_line("determination")
        self.assertEqual(res['eng'], "determination")
        self.assertEqual(res['cn'], "待翻译")
        self.assertEqual(res['needs_translation'], True)

    def test_mixed_content(self):
        res = parse_line("apple 苹果")
        self.assertEqual(res['eng'], "apple")
        self.assertEqual(res['cn'], "苹果")
        self.assertEqual(res['needs_translation'], False)

    def test_complex_chinese(self):
        res = parse_line("ecology 生态学 环境")
        self.assertEqual(res['eng'], "ecology")
        self.assertEqual(res['cn'], "生态学 环境")
        self.assertEqual(res['needs_translation'], False)

if __name__ == '__main__':
    unittest.main()