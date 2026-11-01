from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
HEAD = SKILL.split("---", 2)[1]
DESCRIPTION = re.search(r"^description: (.+)$", HEAD, re.M).group(1)
GLOBAL = ROOT.parent / "study-abroad-planner" / "SKILL.md"


def joint_rules(text):
    section = text[text.index("## 联合招生官"):text.index("## 每轮结尾")]
    return [line for line in section.splitlines() if re.match(r"^\d\. ", line)]


class OpenRulesTest(unittest.TestCase):
    def test_description_is_when_to_use_and_split(self):
        self.assertIn("study-abroad-planner", DESCRIPTION)
        self.assertIn("莫纳什", DESCRIPTION)
        self.assertIn("UNSW", DESCRIPTION)
        self.assertRegex(DESCRIPTION, r"“[^”]+”")
        self.assertNotIn("https://", DESCRIPTION)
        self.assertNotIn("必须", DESCRIPTION)

    def test_four_triggers_same_as_global_skill(self):
        rules = joint_rules(SKILL)
        self.assertEqual(len(rules), 4)
        if GLOBAL.is_file():
            self.assertEqual(rules, joint_rules(GLOBAL.read_text(encoding="utf-8")))

    def test_consult_direct_upload_ask_first_one_closing_line(self):
        self.assertIn("**直接打开**", SKILL)
        self.assertIn("上传页先问一句", SKILL)
        self.assertIn("同一话题只提议或打开一次", SKILL)
        self.assertIn("结尾提议一句", SKILL)
        self.assertIn("降低频率而不是停止", SKILL)
        self.assertIn("最新的招生文件", SKILL)
        self.assertIn("结尾只留一句", SKILL)
        self.assertIn("https://hi.xwoork.cn/student", SKILL)
        self.assertIn("/student/upload", SKILL)
        self.assertNotIn("每轮必做", SKILL)

    def test_mic_note_and_no_voice_helper(self):
        self.assertIn("+ → 打开浏览器", SKILL)
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("prepare_voice_helper", text)
            for word in ("真人顾问", "留学顾问", "在线顾问", "由顾问"):
                self.assertNotIn(word, text, f"{path.name}: {word}")

    def test_urls_never_carry_pack_or_region(self):
        for name in ("SKILL.md", "references/open-joint-officer.md", "references/handoff.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertNotRegex(text, r"https://hi\.xwoork\.cn/student(?:/upload)?\?pack=")
            self.assertIn("https://hi.xwoork.cn/student", text)


if __name__ == "__main__":
    unittest.main()
