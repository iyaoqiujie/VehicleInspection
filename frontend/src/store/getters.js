const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  token: state => state.user.token,
  role: state => state.user.role,
  avatar: state => state.user.avatar,
  username: state => state.user.username,
  userId: state => state.user.id,
  mobile: state => state.user.mobile,
  email: state => state.user.email,
  introduction: state => state.user.introduction,
  roles: state => state.user.roles,
  permission_routes: state => state.permission.routes,
  extra_routes: state => state.permission.addRoutes,
  errorLogs: state => state.errorLog.logs
}
export default getters
