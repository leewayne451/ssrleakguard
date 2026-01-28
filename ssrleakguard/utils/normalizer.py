def normalize_ssr_data(data):
    """
    Remove or normalize fields that change per request
    to reduce diff noise.
    """
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if key in {
                "buildId",
                "__N_SSP",
                "__N_SSG",
                "runtimeConfig",
            }:
                continue
            cleaned[key] = normalize_ssr_data(value)
        return cleaned

    if isinstance(data, list):
        return [normalize_ssr_data(item) for item in data]

    return data