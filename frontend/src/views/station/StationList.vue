<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="名称、地址、联系人、联系人电话" style="width: 250px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        新增检测点
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        导出文件
      </el-button>
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
      @sort-change="sortChange"
    >
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column type="index" label="编号" width="80">
      </el-table-column>
      <el-table-column prop="id" v-if="0">
      </el-table-column>
      <el-table-column prop="name" label="检测点名称" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="contact" label="联系人" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="phone" label="联系人电话" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="address" label="地址" min-width="10%" align="center">
      </el-table-column>
      <el-table-column prop="admin_username" label="管理员用户名" min-width="10%" align="center">
      </el-table-column>
      <el-table-column label="动作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            修改
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="检测点管理员" prop="stationadmin">
          <el-input v-model="temp.stationadmin" type="text" placeholder="检测点管理员的用户名或者手机号"
                    :readonly="dialogStatus==='update'"/>
        </el-form-item>
        <el-form-item label="检测点名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="检测点地址" prop="address">
          <el-input v-model="temp.address" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact">
          <el-input v-model="temp.contact" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="temp.phone" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { userList } from '@/api/user'
import { stationList, addStation, updateStation } from '@/api/station'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'StationTable',
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
    const validateAdminUser = (rule, value, callback) => {
      if (value === '') {
        this.$message({
          message: '需要填写检测点管理员用户名或手机号',
          type: 'error'
        })
        callback(new Error('需要填写检测点管理员用户名或手机号'))
      } else {
        userList({ page: 1, limit: 5, search: value }).then(response => {
          if (response.count === 0) {
            this.$message({
              message: '用户:' + value + ' 不存在',
              type: 'error'
            })
            callback(new Error('用户:' + value + ' 不存在'))
          } else if (response.count > 1) {
            this.$message({
              message: '用户名:' + value + ' 错误， 请检查用户名是否输入错误',
              type: 'error'
            })
            callback(new Error('用户名:' + value + ' 错误， 请检查用户名是否输入错误'))
          } else if (response.results[0].role !== 'STATIONADMIN') {
            this.$message({
              message: value + '不是检测点管理员，请重新输入',
              type: 'error'
            })
            callback(new Error(value + '不是检测点管理员，请重新输入'))
          }
        })
        callback()
      }
    }
    return {
      tableKey: 0,
      list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: '',
        ordering: '-created'
      },
      sortOptions: [{ label: '创建时间升序', key: 'created' }, { label: '创建时间降序', key: '-created' }],
      temp: {
        id: undefined,
        name: '',
        contact: '',
        phone: '',
        address: '',
        stationadmin: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改检测点',
        create: '创建检测点'
      },
      rules: {
        name: [{ required: true, message: '需要填写检测点名称', trigger: 'blur' }],
        address: [{ required: true, message: '需要填写检测点地址', trigger: 'blur' }],
        stationadmin: [{ validator: validateAdminUser, trigger: 'blur', required: true }]
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
      stationList(this.listQuery).then(response => {
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
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        name: '',
        contact: '',
        phone: '',
        address: '',
        stationadmin: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      const _this = this
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            addStation(this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建检测点成功',
                type: 'success',
                duration: 1000
              })
              this.getList()
            }).catch(error => {
              console.log('rejected: ', error)
              this.$message({
                message: '创建检测点失败',
                type: 'error'
              })
              _this.dialogFormVisible = false
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.stationadmin = row.admin_username
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      const _this = this
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            updateStation(tempData.id, tempData).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '修改检测点信息成功',
                type: 'success',
                duration: 1000
              })
              this.getList()
            }).catch(error => {
              console.log('rejected: ', error)
              this.$message({
                message: '修改检测点信息失败',
                type: 'error'
              })
              _this.dialogFormVisible = false
            })
          })
        }
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
