"""Simulated multi-turn student conversation against the joint admissions officer rules.

The keyword model mirrors SKILL.md: doubt/challenge, repeated not-understanding, submission
requests and plan finalisation open the consult page directly; school questions, material lists
and plan deliveries get one closing offer; after a refusal or "别再弹" the page is no longer opened
proactively, but every answer carries the one-click link and direct requests still open it.
"""
from __future__ import annotations
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
LINK = "[一键咨询联合招生官](https://hi.xwoork.cn/student)"

REFUSE = ("不用了", "别再弹", "不要", "我自己去官网", "我先自己准备")
PERSON = ("真人", "顾问", "找联合招生官", "在线咨询")
DOUBT = ("网上说", "乱说", "靠谱吗", "不可信", "担心", "不放心")
CONFUSED = ("听不懂", "不明白", "搞不清楚")
SUBMIT = ("怎么递交", "在哪提交", "在哪里提交", "帮我申请", "帮忙申请", "直接帮我申", "交到平台", "确认递交")
FINAL = ("就按这个方案来吧", "按这个来", "就按这个", "定了", "就这样吧", "没问题了", "确定了")
END = ("谢谢，先这样", "先这样吧")
SCHOOLS = ("莫纳什", "墨尔本", "UNSW", "新南", "悉尼大学", "ANU", "昆士兰", "西澳", "阿德莱德")


class Conversation:
    def __init__(self):
        self.explained = False   # a "听不懂" was already answered with a simpler explanation
        self.muted = False       # student refused or said 别再弹
        self.plan_edits = 0

    def turn(self, text):
        """Return (action, link_appended). action: open / ask_upload / offer / answer / end."""
        if any(w in text for w in END):
            return "end", False
        if any(w in text for w in REFUSE):
            self.muted = True
            return "answer", True
        action = self._action(text)
        if self.muted and action == "offer":
            action = "answer"  # lower frequency: no proactive offer, the link stays
        return action, self.muted and action != "open"

    def _action(self, text):
        if any(w in text for w in ("交到平台", "确认递交", "免费协助")):
            return "ask_upload"
        if any(w in text for w in PERSON + DOUBT + SUBMIT + FINAL):
            return "open"
        if any(w in text for w in CONFUSED):
            if self.explained:
                return "open"
            self.explained = True
            return "answer"  # first time: re-explain in simpler words
        if "改" in text and "方案" in text or "少2万" in text:
            self.plan_edits += 1
            return "offer" if self.plan_edits >= 2 else "answer"
        if "怎么申请" in text:
            return "answer"  # process question, not a submission request
        if any(w in text for w in ("材料", "方案")) or any(s in text for s in SCHOOLS):
            return "offer"
        return "answer"


class SimulatedStudentTest(unittest.TestCase):
    def check(self, turns):
        convo = Conversation()
        for text, expected, link in turns:
            self.assertEqual(convo.turn(text), (expected, link), text)

    def test_report_a_sentences(self):
        self.check([
            ("GPA3.2能上莫纳什吗", "offer", False),
            ("UNSW商科雅思要几分", "offer", False),
            ("墨尔本大学和悉尼大学读会计哪个好", "offer", False),
            ("澳洲八大预科怎么申请", "answer", False),
            ("你说的我听不懂", "answer", False),
            ("还是听不懂", "open", False),
            ("网上说ANU很难进，你是不是乱说", "open", False),
            ("我想找个真人聊聊", "open", False),
            ("ANU研究型硕士要找导师吗", "offer", False),
            ("我国内本科，想申墨尔本硕士，要交哪些材料", "offer", False),
            ("能不能直接帮我申请墨尔本", "open", False),
            ("网上说八大学费都能免，靠谱吗", "open", False),
            ("这个方案预算太高，帮我改一下，少2万", "answer", False),
            ("再改一下方案，换成悉尼", "offer", False),
            ("就按这个方案来吧", "open", False),
            ("谢谢，先这样吧", "end", False),
        ])

    def test_muted_lowers_frequency_but_keeps_link_and_direct_requests(self):
        self.check([
            ("别再弹窗了", "answer", True),
            ("墨尔本会计硕士学费多少", "answer", True),   # no proactive offer, link appended
            ("不用了，我自己官网申", "answer", True),
            ("我想找个真人聊聊", "open", False),          # student asks: open as usual
            ("定了，就这样吧", "open", False),
            ("好的确认递交，联合招生官免费协助", "ask_upload", True),
        ])

    def test_skill_text_backs_the_model(self):
        for phrase in ("你是不是乱说", "就按这个方案来吧", "第一次说“听不懂”先", "只问“怎么申请/申请流程”先答流程",
                       "第一次小修改不提议", "本轮需要学生补信息时只问信息", LINK):
            self.assertIn(phrase, SKILL)
        self.assertNotIn("pack=", SKILL)
        self.assertIn("start_intake", (ROOT / "references" / "handoff.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
