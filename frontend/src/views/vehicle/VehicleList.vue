<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="车牌号、车辆识别代码、绑定用户手机号" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.character" placeholder="使用性质" clearable style="width: 120px" class="filter-item">
        <el-option v-for="item in characterOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.ordering" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        新增车辆
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
      <el-table-column prop="bounduser_mobile" label="绑定用户手机号" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="plate" label="车牌号" min-width="10%" align="center">
      </el-table-column>
      <el-table-column prop="vin" label="车辆识别代码" min-width="10%" align="center">
      </el-table-column>
      <el-table-column prop="vtype" label="车辆类型" min-width="15%" align="center">
      </el-table-column>
      <el-table-column prop="owner" label="所有人" min-width="10%" align="center">
      </el-table-column>
      <el-table-column prop="character" label="使用性质" min-width="10%" align="center" :formatter="formatCharacter">
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
        <el-form-item label="绑定用户手机号" prop="bounduser_mobile">
          <el-input v-model="temp.bounduser_mobile" />
        </el-form-item>
        <el-form-item label="车牌号" prop="plate">
          <el-input v-model="temp.plate" />
        </el-form-item>
        <el-form-item label="车辆识别代码" prop="vin">
          <el-input v-model="temp.vin" />
        </el-form-item>
        <el-form-item label="车辆类型" prop="vtype">
          <el-input v-model="temp.vtype" />
        </el-form-item>
        <el-form-item label="所有人" prop="owner">
          <el-input v-model="temp.owner" />
        </el-form-item>
        <el-form-item label="使用性质" prop="character">
          <el-select v-model="temp.character" class="filter-item" placeholder="Please select">
            <el-option v-for="item in characterOptions" :key="item.key" :label="item.label" :value="item.key" />
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
import { vehiList, addVehi, updateVehi } from '@/api/vehicle'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'VehicleTable',
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
        character: '',
        ordering: '-created'
      },
      characterOptions: [{ key: 1, label: '非营运' }, { key: 2, label: '营运' }],
      sortOptions: [{ label: '创建时间升序', key: 'created' }, { label: '创建时间降序', key: '-created' }],
      scheduledDatePicker: this.scheduledDate(),
      temp: {
        id: undefined,
        bounduser_mobile: '',
        plate: '',
        vin: '',
        vtype: '',
        owner: '',
        character: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      rules: {
        username: [{ required: true, message: 'type is required', trigger: 'change' }],
        mobile: [{ required: true, message: 'timestamp is required', trigger: 'change' }],
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    formatCharacter: (row, column) => {
      if (row.character === 1) {
        return '非营运'
      } else {
        return '营运'
      }
    },
    scheduledDate() {
      return {
        disabledDate(time) {
          const currDate = (new Date()).getTime()
          return time.getTime() < currDate
        }
      }
    },
    getList() {
      this.listLoading = true
      this.listQuery.offset = (this.listQuery.page - 1) * this.listQuery.limit
      vehiList(this.listQuery).then(response => {
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
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        bounduser_mobile: '',
        plate: '',
        vin: '',
        vtype: '',
        owner: '',
        character: ''
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
            addVehi(this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建车辆成功',
                type: 'success',
                duration: 1000
              })
              this.getList()
            }).catch(error => {
              console.log('rejected: ', error)
              this.$message({
                message: '创建车辆失败',
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
            updateVehi(tempData.id, tempData).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '修改车辆信息成功',
                type: 'success',
                duration: 1000
              })
              this.getList()
            }).catch(error => {
              console.log('rejected: ', error)
              this.$message({
                message: '修改车辆信息失败',
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
        const tHeader = ['绑定用户手机号', '车牌号', '车辆识别代码', '车辆类型', '所有人', '使用性质']
        const filterVal = ['bounduser_mobile', 'plate', 'vin', 'vtype', 'owner', 'character']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: '机动车列表'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'character') {
          if (v[j] === 1) {
            return '非营运'
          } else {
            return '营运'
          }
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
