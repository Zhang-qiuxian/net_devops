import pandas as pd


def handle_tojson(data: dict[str, list]) -> list[dict]:
    """数据处理"""
    try:
        df = pd.DataFrame(data)
        to_json = df.to_dict(orient="records")
        return to_json
    except Exception as e:
        return None


def handle_mac(data: list[str]) -> list[str]:
    """处理mac地址"""
    return [i.strip('"').replace(" ", ":").lower()[:-1] for i in data]


def handel_symbol_list(data: list[str]) -> list[str]:
    """处理字符串"""
    return [i.strip('"') for i in data]


def handel_symbol_dict(data: dict) -> dict:
    """处理字符串"""
    return {k: v[0].strip('"').strip() for k, v in data.items()}
