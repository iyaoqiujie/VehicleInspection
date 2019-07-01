const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  token: state => state.user.token,
  usertype: state => state.user.usertype,
  avatar: state => state.user.avatar,
  name: state => state.user.username,
  mobile: state => state.user.mobile,
  introduction: state => state.user.introduction,
  roles: state => state.user.roles,
  permission_routes: state => state.permission.routes,
  extra_routes: state => state.permission.addRoutes,
  errorLogs: state => state.errorLog.logs
}
export default getters
