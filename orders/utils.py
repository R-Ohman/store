import re

from orders.models import Refund


def update_refund_status_to_refunded(queryset=None):
    for refund in queryset:
        refund.status = Refund.REFUNDED
        refund.save()
    # send message to user


def validate_postal_code(country_code, postal_code):
    postal_code_patterns = {
        "gb": r"GIR[ ]?0AA|((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\d{1,4}",
        "je": r"JE\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}",
        "gg": r"GY\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}",
        "im": r"IM\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}",
        "us": r"\d{5}([ \-]\d{4})?",
        "ca": r"[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d",
        "de": r"\d{5}",
        "jp": r"\d{3}-\d{4}",
        "fr": r"\d{2}[ ]?\d{3}",
        "au": r"\d{4}",
        "it": r"\d{5}",
        "ch": r"\d{4}",
        "at": r"\d{4}",
        "es": r"\d{5}",
        "nl": r"\d{4}[ ]?[A-Z]{2}",
        "be": r"\d{4}",
        "dk": r"\d{4}",
        "se": r"\d{3}[ ]?\d{2}",
        "no": r"\d{4}",
        "br": r"\d{5}[\-]?\d{3}",
        "pt": r"\d{4}([\-]\d{3})?",
        "fi": r"\d{5}",
        "ax": r"22\d{3}",
        "kr": r"\d{3}[\-]\d{3}",
        "cn": r"\d{6}",
        "tw": r"\d{3}(\d{2})?",
        "sg": r"\d{6}",
        "dz": r"\d{5}",
        "ad": r"AD\d{3}",
        "ar": r"([A-HJ-NP-Z])?\d{4}([A-Z]{3})?",
        "am": r"(37)?\d{4}",
        "az": r"\d{4}",
        "bh": r"((1[0-2]|[2-9])\d{2})?",
        "bd": r"\d{4}",
        "bb": r"(BB\d{5})?",
        "by": r"\d{6}",
        "bm": r"[A-Z]{2}[ ]?[A-Z0-9]{2}",
        "ba": r"\d{5}",
        "io": r"BBND 1ZZ",
        "bn": r"[A-Z]{2}[ ]?\d{4}",
        "bg": r"\d{4}",
        "kh": r"\d{5}",
        "cv": r"\d{4}",
        "cl": r"\d{7}",
        "cr": r"\d{4,5}|\d{3}-\d{4}",
        "hr": r"\d{5}",
        "cy": r"\d{4}",
        "cz": r"\d{3}[ ]?\d{2}",
        "do": r"\d{5}",
        "ec": r"([A-Z]\d{4}[A-Z]|(?:[A-Z]{2})?\d{6})?",
        "eg": r"\d{5}",
        "ee": r"\d{5}",
        "fo": r"\d{3}",
        "ge": r"\d{4}",
        "gr": r"\d{3}[ ]?\d{2}",
        "gl": r"39\d{2}",
        "gt": r"\d{5}",
        "ht": r"\d{4}",
        "hn": r"(?:\d{5})?",
        "hu": r"\d{4}",
        "is": r"\d{3}",
        "in": r"\d{6}",
        "id": r"\d{5}",
        "il": r"\d{5}",
        "jo": r"\d{5}",
        "kz": r"\d{6}",
        "ke": r"\d{5}",
        "kw": r"\d{5}",
        "la": r"\d{5}",
        "lv": r"\d{4}",
        "lb": r"(\d{4}([ ]?\d{4})?)?",
        "li": r"(948[5-9])|(949[0-7])",
        "lt": r"\d{5}",
        "lu": r"\d{4}",
        "mk": r"\d{4}",
        "my": r"\d{5}",
        "mv": r"\d{5}",
        "mt": r"[A-Z]{3}[ ]?\d{2,4}",
        "mu": r"(\d{3}[A-Z]{2}\d{3})?",
        "mx": r"\d{5}",
        "md": r"\d{4}",
        "mc": r"980\d{2}",
        "ma": r"\d{5}",
        "np": r"\d{5}",
        "nz": r"\d{4}",
        "ni": r"((\d{4}-)?\d{3}-\d{3}(-\d{1})?)?",
        "ng": r"(\d{6})?",
        "om": r"(PC )?\d{3}",
        "pk": r"\d{5}",
        "py": r"\d{4}",
        "ph": r"\d{4}",
        "pl": r"\d{2}-\d{3}",
        "pr": r"00[679]\d{2}([ \-]\d{4})?",
        "ro": r"\d{6}",
        "ru": r"\d{6}",
        "sm": r"4789\d",
        "sa": r"\d{5}",
        "sn": r"\d{5}",
        "sk": r"\d{3}[ ]?\d{2}",
        "si": r"\d{4}",
        "za": r"\d{4}",
        "lk": r"\d{5}",
        "tj": r"\d{6}",
        "th": r"\d{5}",
        "tn": r"\d{4}",
        "tr": r"\d{5}",
        "tm": r"\d{6}",
        "ua": r"\d{5}",
        "uy": r"\d{5}",
        "uz": r"\d{6}",
        "va": r"00120",
        "ve": r"\d{4}",
        "zm": r"\d{5}",
        "as": r"96799",
        "cc": r"6799",
        "ck": r"\d{4}",
        "rs": r"\d{6}",
        "me": r"8\d{4}",
        "cs": r"\d{5}",
        "yu": r"\d{5}",
        "cx": r"6798",
        "et": r"\d{4}",
        "fk": r"FIQQ 1ZZ",
        "nf": r"2899",
        "fm": r"(9694[1-4])([ \-]\d{4})?",
        "gf": r"9[78]3\d{2}",
        "gn": r"\d{3}",
        "gp": r"9[78][01]\d{2}",
        "gs": r"SIQQ 1ZZ",
        "gu": r"969[123]\d([ \-]\d{4})?",
        "gw": r"\d{4}",
        "hm": r"\d{4}",
        "iq": r"\d{5}",
        "kg": r"\d{6}",
        "lr": r"\d{4}",
        "ls": r"\d{3}",
        "mg": r"\d{3}",
        "mh": r"969[67]\d([ \-]\d{4})?",
        "mn": r"\d{6}",
        "mp": r"9695[012]([ \-]\d{4})?",
        "mq": r"9[78]2\d{2}",
        "nc": r"988\d{2}",
        "ne": r"\d{4}",
        "vi": r"008(([0-4]\d)|(5[01]))([ \-]\d{4})?",
        "pf": r"987\d{2}",
        "pg": r"\d{3}",
        "pm": r"9[78]5\d{2}",
        "pn": r"PCRN 1ZZ",
        "pw": r"96940",
        "re": r"9[78]4\d{2}",
        "sh": r"(ASCN|STHL) 1ZZ",
        "sj": r"\d{4}",
        "so": r"\d{5}",
        "sz": r"[HLMS]\d{3}",
        "tc": r"TKCA 1ZZ",
        "wf": r"986\d{2}",
        "xk": r"\d{5}",
        "yt": r"976\d{2}",
    }

    if country_code in postal_code_patterns:
        pattern = postal_code_patterns[country_code]
        return bool(re.match(pattern, postal_code))
    return False
