import request from '@/utils/request'

export function orderList(query) {
  return request({
    url: '/vinsp/appmnt/order/',
    method: 'get',
    params: query
  })
}

export function fetchOrder(id) {
  return request({
    url: '/vinsp/appmnt/order/' + id + '/',
    method: 'get'
  })
}

export function addOrder(data) {
  return request({
    url: '/vinsp/appmnt/order/',
    method: 'post',
    data
  })
}

export function updateOrder(id, data) {
  return request({
    url: '/vinsp/appmnt/order/' + id + '/',
    method: 'put',
    data
  })
}
