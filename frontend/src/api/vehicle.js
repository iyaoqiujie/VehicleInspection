import request from '@/utils/request'

export function vehiList(query) {
  return request({
    url: '/vinsp/vehicle/vehi/',
    method: 'get',
    params: query
  })
}

export function fetchVehi(id) {
  return request({
    url: '/vinsp/vehicle/vehi/' + id + '/',
    method: 'get'
  })
}

export function addVehi(data) {
  return request({
    url: '/vinsp/vehicle/vehi/',
    method: 'post',
    data
  })
}

export function updateVehi(id, data) {
  return request({
    url: '/vinsp/vehicle/vehi/' + id + '/',
    method: 'put',
    data
  })
}
