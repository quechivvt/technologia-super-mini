class TokenBlacklistKey:

    @staticmethod
    def blacklist(jti: str) -> str:
        return f"blacklist:{jti}"