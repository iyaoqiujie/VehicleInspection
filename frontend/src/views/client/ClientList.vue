<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="用户名、手机号" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.usertype" placeholder="用户类型" clearable style="width: 120px" class="filter-item">
        <el-option v-for="item in usertypeOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.is_certificated" placeholder="实名认证" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in certOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        新增用户
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
      <el-table-column v-if="0" prop="id">
      </el-table-column>
      <el-table-column prop="username" label="用户名" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="mobile" label="手机" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="usertype" label="用户类型" min-width="10%" align="center" :formatter="formatUsertype">
      </el-table-column>
      <el-table-column prop="is_certificated" label="实名认证" min-width="10%" align="center" :formatter="formatIsCerted">
      </el-table-column>
      <el-table-column prop="can_order" label="能否预约" min-width="10%" align="center" :formatter="formatCanOrder">
      </el-table-column>
      <el-table-column prop="company" label="所属公司" min-width="10%" align="center">
      </el-table-column>
      <el-table-column prop="email" label="电子邮件" min-width="10%" align="center">
      </el-table-column>
      <el-table-column label="动作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button-group>
            <el-button type="primary" icon="el-icon-edit" size="small" @click="handleUpdate(row)">
              修改
            </el-button>
            <el-button v-if="row.can_order" icon="el-icon-close" size="small" type="danger" @click="switchCanOrder(row)">
              禁止预约
            </el-button>
            <el-button v-if="!row.can_order" icon="el-icon-check" size="small" type="success" @click="switchCanOrder(row)">
              开放预约
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="temp.username" />
        </el-form-item>
        <el-form-item label="手机号" prop="mobile">
          <el-input v-model="temp.mobile" />
        </el-form-item>
        <el-form-item label="电子邮件" prop="email">
          <el-input v-model="temp.email" />
        </el-form-item>
        <el-form-item label="所属公司" prop="company">
          <el-input v-model="temp.company" />
        </el-form-item>
        <el-form-item label="用户类型" prop="usertype">
          <el-select v-model="temp.usertype" class="filter-item" placeholder="请选择...">
            <el-option v-for="item in usertypeOptions" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="实名认证" prop="is_certificated">
          <el-select v-model="temp.is_certificated" class="filter-item" placeholder="请选择...">
            <el-option v-for="item in certOptions" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
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
import { userList, addUser, updateUser } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'UserTable',
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
        limit: 100,
        search: '',
        usertype: '',
        is_certificated: '',
        ordering: '-date_joined'
      },
      certOptions: [{ label: '已认证', key: true }, { label: '未认证', key: false }],
      usertypeOptions: [
        { label: '超级管理员', key: 'SUPERADMIN' },
        { label: '检测点管理员', key: 'STATIONADMIN' },
        { label: '普通用户', key: 'CLIENT' },
      ],
      sortOptions: [{ label: '创建时间升序', key: 'date_joined' }, { label: '创建时间降序', key: '-date_joined' }],
      temp: {
        id: undefined,
        username: '',
        name: '',
        mobile: '',
        email: '',
        company: '',
        usertype: '',
        is_certificated: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      rules: {
        username: [{ required: true, message: '需要填写用户名', trigger: 'change' }],
        mobile: [{ required: true, message: '需要填写手机号', trigger: 'change' }],
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    formatUsertype: (row, column) => {
      if (row.usertype === 'SUPERADMIN') {
        return '超级管理员'
      } else if (row.usertype === 'STATIONADMIN') {
        return '检测点管理员'
      } else {
        return '普通用户'
      }
    },
    formatIsCerted: (row, column) => {
      return row.is_certificated ? '已认证' : '未认证'
    },
    formatCanOrder: (row, column) => {
      return row.can_order ? '可预约' : '待审核'
    },
    getList() {
      this.listLoading = true
      this.listQuery.offset = (this.listQuery.page - 1) * this.listQuery.limit
      console.log(this.listQuery.offset)
      userList(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    switchCanOrder(row) {
      const data = { 'can_order': !row.can_order }
      this.$confirm('确认修改吗？', '提示', {}).then(() => {
        updateUser(row.id, data).then(() => {
          this.$message({
            message: '操作成功',
            type: 'success'
          })
          this.getList()
        }).catch(error => {
          console.log('rejected: ', error)
          this.$message({
            message: '修改用户信息失败',
            type: 'error'
          })
        })
      })
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
        username: '',
        name: '',
        mobile: '',
        email: '',
        company: '',
        usertype: '',
        is_certificated: undefined
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
            addUser(this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建用户成功',
                type: 'success',
                duration: 1000
              })
              this.getList()
            }).catch(error => {
              console.log('rejected: ', error)
              this.$message({
                message: '创建用户失败',
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
      console.log(this.temp)
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
            updateUser(tempData.id, tempData).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '修改用户信息成功',
                type: 'success',
                duration: 1000
              })
              this.getList()
            }).catch(error => {
              console.log('rejected: ', error)
              this.$message({
                message: '修改用户信息失败',
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
        const tHeader = ['用户名', '手机号', '用户类型', '电子邮件', '所属公司', '实名认证', '可预约']
        const filterVal = ['username', 'mobile', 'usertype', 'email', 'compmay', 'is_certificated', 'can_order']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: '用户列表'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
