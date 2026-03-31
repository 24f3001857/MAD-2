from .auth_apis import LoginUser, SignUpUser, LogoutUser
from .profile_api import ProfileAPI
from .admin_api import AdminStatsAPI

def init_api(api):
    api.add_resource(LoginUser, '/login')
    api.add_resource(SignUpUser, '/signup')
    api.add_resource(LogoutUser, '/logout')
    api.add_resource(ProfileAPI, '/profile')
    api.add_resource(AdminStatsAPI, '/admin/stats')
    return api