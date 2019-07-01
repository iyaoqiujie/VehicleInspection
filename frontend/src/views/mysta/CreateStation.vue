<template>
  <div class="app-container">
    <el-form ref="stationForm" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="检测点管理员" prop="admin_username">
        <el-input v-model="form.admin_username" type="text" placeholder="请输入检测点管理员的用户名或者手机号" />
      </el-form-item>
      <el-form-item label="检测点名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="检测点地址" prop="address">
        <el-input v-model="form.address" />
      </el-form-item>
      <el-form-item label="联系人姓名">
        <el-input v-model="form.contact" />
      </el-form-item>
      <el-form-item label="联系人电话">
        <el-input v-model="form.phone" />
      </el-form-item>
      <!--
      <el-form-item label="上午检测时间">
        <el-col :span="11">
          <el-time-select v-model="form.am_start_time" placeholder="开始时间" style="width: 100%;"
                          :picker-options="{start: '08:00', step: '00:30', end: '10:00'}"/>
        </el-col>
        <el-col :span="2" class="line">-</el-col>
        <el-col :span="11">
          <el-time-select v-model="form.am_end_time" placeholder="结束时间" style="width: 100%;"
                          :picker-options="{start: '10:00', step: '00:30', end: '12:00'}"/>
        </el-col>
      </el-form-item>
      <el-form-item label="下午检测时间">
        <el-col :span="11">
          <el-time-select v-model="form.pm_start_time" placeholder="开始时间" style="width: 100%;"
                          :picker-options="{start: '12:30', step: '00:30', end: '14:00'}"/>
        </el-col>
        <el-col :span="2" class="line">-</el-col>
        <el-col :span="11">
          <el-time-select v-model="form.pm_end_time" placeholder="结束时间" style="width: 100%;"
                          :picker-options="{start: '15:00', step: '00:30', end: '19:00'}"/>
        </el-col>
      </el-form-item>
      <el-form-item label="检测时间间隔">
        <el-select v-model="form.interval" placeholder="设置检测时间间隔">
          <el-option v-for="item in intervalOptions" :key="item.key" :label="item.label" :value="item.key">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="截止预约时间">
        <el-col :span="11">
          <el-time-select v-model="form.cutoff_time" placeholder="截止预约时间" style="width: 100%;"
                          :picker-options="{start: '15:00', step: '00:30', end: '17:00'}"/>
        </el-col>
      </el-form-item>
      <el-form-item label="最大预约数">
        <el-col :span="11">
          <el-input type="text" v-model="form.threshhold"  placeholder="请设置单个时间段最大预约数, 默认 20"/>
        </el-col>
      </el-form-item>
      <el-form-item label="Instant delivery">
        <el-switch v-model="form.delivery" />
      </el-form-item>
      <el-form-item label="Activity type">
        <el-checkbox-group v-model="form.type">
          <el-checkbox label="Online activities" name="type" />
          <el-checkbox label="Promotion activities" name="type" />
          <el-checkbox label="Offline activities" name="type" />
          <el-checkbox label="Simple brand exposure" name="type" />
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="Resources">
        <el-radio-group v-model="form.resource">
          <el-radio label="Sponsor" />
          <el-radio label="Venue" />
        </el-radio-group>
      </el-form-item>
      -->
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { userList } from '@/api/user'
import { addStation } from '@/api/station'

export default {
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
          this.list = response.results
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
          } else if (response.results[0].usertype != 'STATIONADMIN') {
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
      form: {
        admin_username: '',
        name: '',
        address: '',
        contact: '',
        phone: '',
        region: '',
        am_start_time: '08:00',
        am_end_time: '11:00',
        pm_start_time: '13:00',
        pm_end_time: '17:00',
        cutoff_time: '15:00',
        interval: 60,
        threshhold: 20,
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      },
      intervalOptions: [
        { key: 60, label: '1 小时' },
        { key: 90, label: '90 分钟' },
        { key: 120, label: '2 小时' }
      ],
      rules: {
        name: [{ required: true, message: '需要填写检测点名称', trigger: 'blur' }],
        address: [{ required: true, message: '需要填写检测点地址', trigger: 'blur' }],
        admin_username: [{ validator: validateAdminUser, trigger: 'blur', required: true }]
      }
    }
  },
  methods: {
    onSubmit() {
      const _this = this
      this.$refs['stationForm'].validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.$message('submit!')
            addStation(this.form).then(() => {
              this.$notify({
                title: '成功',
                message: '创建检测站成功',
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
            })
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

