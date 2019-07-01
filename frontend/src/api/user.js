import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/vinsp/token-auth/',
    method: 'post',
    data
  })
}

export function userList(query) {
  return request({
    url: '/vinsp/acct/users/',
    method: 'get',
    params: query
  })
}

export function fetchUser(id) {
  return request({
    url: '/vinsp/acct/users/' + id + '/',
    method: 'get'
  })
}

export function addUser(data) {
  return request({
    url: '/vinsp/acct/addUser/',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: '/vinsp/acct/users/' + id + '/',
    method: 'put',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
