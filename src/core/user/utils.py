from user_agents import parse


def parse_user_agent(user_agent: str):
    if not user_agent:
        return {"orig": user_agent}
    
    parsed = parse(user_agent)
    return {
        "browser": {
            "family": parsed.browser.family,
            "version": parsed.browser.version_string,
        },
        "os": {"family": parsed.os.family, "version": parsed.os.version_string},
        "device": {
            "family": parsed.device.family,
            "brand": parsed.device.brand,
            "model": parsed.device.model,
        },
        "orig": user_agent,
    }