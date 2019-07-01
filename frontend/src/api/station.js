import request from '@/utils/request'

export function stationList(query) {
  return request({
    url: '/vinsp/station/inspstation/',
    method: 'get',
    params: query
  })
}

export function fetchStation(id) {
  return request({
    url: '/vinsp/station/inspstation/' + id + '/',
    method: 'get'
  })
}

export function addStation(data) {
  return request({
    url: '/vinsp/acct/addUser/',
    method: 'post',
    data
  })
}

export function updateStation(id, data) {
  return request({
    url: '/vinsp/station/inspstation/' + id + '/',
    method: 'put',
    data
  })
}
