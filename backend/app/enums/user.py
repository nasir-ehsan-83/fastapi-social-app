from enum import Enum

class UserRole(str, Enum):
    admin: str = "admin"
    super_user: str = "super_user"
    user: str = "user"

class UserStatus(str, Enum):
    active: str = "active"
    inactive : str = "inactive"
    banned: str = "banned"
    suspanded: str = "suspanded"

class UserVisibility(str, Enum):
    public: str = "public"
    private: str = "private"