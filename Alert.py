from __future__ import annotations
import re


def revstr(str):
    return "".join(reversed(str))


class Alert:
    def __init__(self, lines=[]) -> None:
        self.from_lines(lines)

    def from_lines(self, lines):
        splitted = [t.strip() for t in lines]
        self.lines = [t for t in splitted if len(t) > 0]
        return self

    def from_toot(self, toot_content):
        stripped = toot_content.replace("<p>", "").replace("</p>", "").strip()
        splitted = [t for t in stripped.split("<br />")]
        return self.from_lines(splitted)

    def is_same(self, other: Alert):
        # TODO: optimize directly from lines
        return self.text() == other.text()

    def is_in_list(self, list_of_alerts: list[Alert]):
        # TODO: optimize directly from lines
        return any(self.text() == a.text() for a in list_of_alerts)

    def text(self):
        return "\n".join(self.lines).strip()

    def places(self):
        places = [t for t in self.lines if not Alert.reg_date.match(t)]
        places = [t for t in places if all(p not in t for p in Alert.non_places)]
        places = [Alert.reg_paranthesis.sub("", t).strip() for t in places]
        return places

    def show(self, also_places=False):
        """concat lines and reverse each line since hebrew is not shown well"""
        ret = " ".join(l if re.search('[א-ת]', l) is None else revstr(l) for l in self.lines)
        if also_places:
            ret += '\n' + str([revstr(p) for p in self.places()])
        return ret

    non_places = ["ירי רקטות וטילים", "היכנסו למרחב המוגן"]
    reg_date = re.compile("^[0-9:\- ]+$")
    reg_paranthesis = re.compile("\([^)]*\)")
