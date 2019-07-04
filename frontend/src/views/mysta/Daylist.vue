<template>
  <div class="app-container">
    <div class="filter-container">
      <el-date-picker
        v-model="listQuery.daterange"
        type="daterange"
        value-format="yyyy-MM-dd"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        class="filter-item"
        @blur="handleFilter">
      </el-date-picker>
      <el-select v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      stripe
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange">
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column type="index" label="编号" width="80" align="center">
      </el-table-column>
      <el-table-column prop="id" v-if="0">
      </el-table-column>
      <el-table-column prop="day" sortable="custom" label="日期" min-width="10%" align="center">
      </el-table-column>
      <el-table-column prop="weekday" label="星期" min-width="10%" align="center">
      </el-table-column>
      <el-table-column label="能否预约" min-width="10%" align="center">
        <template slot-scope="{row}">
          <el-switch v-model="row.can_order" />
        </template>
      </el-table-column>
      <el-table-column label="备注" min-width="25%" align="center">
        <template slot-scope="{row}">
          <el-input type="text" v-model="row.remark" />
        </template>
      </el-table-column>
      <el-table-column label="动作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="medium" @click="handleUpdate(row)">
            确认修改
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
  </div>
</template>

<script>
import { stationList, addStation, updateStation, stationDayList, updateDay } from '@/api/station'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'StationDayTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: '',
        start: '',
        end: '',
        daterange: '',
        ordering: 'day'
      },
      sortOptions: [{ label: '日期升序', key: 'day' }, { label: '日期降序', key: '-day' }],
      temp: {
        id: undefined,
        day: '',
        weekday: '',
        can_order: true,
        remark: '',
        stationadmin: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改检测点',
        create: '创建检测点'
      },
      rules: {
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      this.listQuery.offset = (this.listQuery.page - 1) * this.listQuery.limit
      this.listQuery.start = this.listQuery.daterange[0]
      this.listQuery.end = this.listQuery.daterange[1]
      stationDayList(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'day') {
        this.sortByDay(order)
      }
    },
    sortByDay(order) {
      if (order === 'ascending') {
        this.listQuery.ordering = 'day'
      } else {
        this.listQuery.ordering = '-day'
      }
      this.handleFilter()
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        updateDay(this.temp.id, this.temp).then(() => {
          this.dialogFormVisible = false
          this.$notify({
            title: '成功',
            message: '修改检测点预约日期成功',
            type: 'success',
            duration: 1000
          })
        }).catch(error => {
          console.log('rejected: ', error)
          this.$message({
            message: '修改检测点预约日期失败',
            type: 'error'
          })
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['管理员用户名', '检测点名称', '联系人', '联系人电话', '地址', '创建时间']
        const filterVal = ['admin_username', 'name', 'contact', 'phone', 'address', 'created']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: '检测点列表'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'created') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
