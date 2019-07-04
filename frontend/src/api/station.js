import request from '@/utils/request'

export function stationList(query) {
  return request({
    url: '/vinsp/station/inspstation/',
    method: 'get',
    params: query
  })
}

export function fetchStationById(id) {
  return request({
    url: '/vinsp/station/inspstation/' + id + '/',
    method: 'get'
  })
}

export function fetchStation() {
  return request({
    url: '/vinsp/station/inspstation/fetch_station/',
    method: 'get'
  })
}

export function stationTimePeriods(id) {
  return request({
    url: '/vinsp/station/inspstation/' + id + '/time_periods/',
    method: 'get'
  })
}

export function addStation(data) {
  return request({
    url: '/vinsp/station/inspstation/',
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

export function fetchRule() {
  return request({
    url: '/vinsp/station/apprule/fetch_rule/',
    method: 'get'
  })
}

export function stationRuleList(query) {
  return request({
    url: '/vinsp/station/apprule/',
    method: 'get',
    params: query
  })
}

export function updateRule(id, data) {
  return request({
    url: '/vinsp/station/apprule/' + id + '/',
    method: 'put',
    data
  })
}

export function fetchDay() {
  return request({
    url: '/vinsp/station/appday/fetch_day/',
    method: 'get'
  })
}

export function stationDayList(query) {
  return request({
    url: '/vinsp/station/appday/',
    method: 'get',
    params: query
  })
}

export function updateDay(id, data) {
  return request({
    url: '/vinsp/station/appday/' + id + '/',
    method: 'put',
    data
  })
}
