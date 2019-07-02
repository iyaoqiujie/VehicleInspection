<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">

      <sticky :z-index="10" :class-name="'sub-navbar '+postForm.status">
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          修改
        </el-button>
      </sticky>

      <div class="createPost-main-container">
        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item style="margin-bottom: 40px;" prop="stationName">
              <MDinput v-model="postForm.station_name" :maxlength="100" name="stationName" readonly>
                检测点名称
              </MDinput>
            </el-form-item>
          </el-col>
        </el-row>

        <div class="postInfo-container">
          <el-row :gutter="20">
            <el-col :span="10">
              <el-form-item label-width="160px" label="上午检测时间 开始: " class="postInfo-container-item">
                <el-time-select v-model="postForm.am_start_time" placeholder="开始时间" style="width: 100%;"
                          :picker-options="{start: '08:00', step: '00:30', end: '10:00'}"/>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label-width="160px" label="结束: " class="postInfo-container-item">
                <el-time-select v-model="postForm.am_end_time" placeholder="结束时间" style="width: 100%;"
                          :picker-options="{start: '10:00', step: '00:30', end: '12:00'}"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="10">
              <el-form-item label-width="160px" label="下午检测时间 开始: " class="postInfo-container-item">
                <el-time-select v-model="postForm.pm_start_time" placeholder="开始时间" style="width: 100%;"
                          :picker-options="{start: '12:30', step: '00:30', end: '14:00'}"/>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label-width="160px" label="结束: " class="postInfo-container-item">
                   <el-time-select v-model="postForm.pm_end_time" placeholder="结束时间" style="width: 100%;"
                          :picker-options="{start: '15:00', step: '00:30', end: '19:00'}"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label-width="160px"  label="检测时间间隔">
            <el-col :span="10">
              <el-select v-model="postForm.interval" placeholder="设置检测时间间隔">
                <el-option v-for="item in intervalOptions" :key="item.key" :label="item.label" :value="item.key">
                </el-option>
              </el-select>
            </el-col>
          </el-form-item>
          <el-form-item label-width="160px"  label="截止预约时间">
            <el-col :span="10">
              <el-time-select v-model="postForm.cutoff_time" placeholder="截止预约时间" style="width: 100%;"
                              :picker-options="{start: '15:00', step: '00:30', end: '17:00'}"/>
            </el-col>
          </el-form-item>
          <el-form-item label-width="160px"  label="最大预约数">
            <el-col :span="10">
              <el-input type="text" v-model="postForm.threshold"  placeholder="请设置单个时间段最大预约数, 默认 20"/>
            </el-col>
          </el-form-item>
        </div>
        <el-row>
          <el-col :span="18">
            <el-form-item  style="margin-bottom: 40px;" label-width="100px" label="检测点管理员">
              <el-input :rows="1" v-model="stationAdminInfo" type="textarea" class="article-textarea" autosize readonly />
            </el-form-item>
          </el-col>
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import MDinput from '@/components/MDinput'
import Sticky from '@/components/Sticky'
import { updateRule, fetchRule } from '@/api/station'

export default {
  name: 'StationRuleDetail',
  components: { MDinput, Sticky },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      postForm: {
        status: 'draft',
        station_name: '',
        station: undefined,
        am_start_time: '08:00',
        am_end_time: '11:00',
        pm_start_time: '13:00',
        pm_end_time: '17:00',
        cutoff_time: '15:00',
        interval: 60,
        threshold: 20,
        id: undefined
      },
      stationAdminInfo: '',
      loading: false,
      intervalOptions: [
        { key: 60, label: '1 小时' },
        { key: 90, label: '90 分钟' },
        { key: 120, label: '2 小时' }
      ],
      rules: {}
    }
  },
  computed: {
    ...mapGetters([
      'mobile',
      'name'
    ])
  },
  created() {
    this.stationAdminInfo = this.name + ' (' + this.mobile + ')'
    this.fetchData()
  },
  methods: {
    fetchData() {
      fetchRule().then(response => {
        if (response.id) {
          this.postForm.id = response.id
          this.postForm.station = response.station_id
          this.postForm.station_name = response.station_name
          this.postForm.am_start_time = response.am_start_time
          this.postForm.am_end_time = response.am_end_time
          this.postForm.pm_start_time = response.pm_start_time
          this.postForm.pm_end_time = response.pm_end_time
          this.postForm.cutoff_time = response.cutoff_time
          this.postForm.interval = response.interval
          this.postForm.threshold = response.threshold
        }
      }).catch(err => {
        console.log(err)
      })
    },
    submitForm() {
      console.log(this.postForm)
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.loading = true
            updateRule(this.postForm.id, this.postForm).then(() => {
              this.loading = false
              this.$notify({
                title: '成功',
                message: '修改预约规则成功',
                type: 'success',
                duration: 1000
              })
              this.fetchData()
            }).catch(error => {
              console.log('rejected: ', error)
              this.loading = false
              this.$message({
                message: '修改预约规则失败',
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

<style lang="scss" scoped>
@import "~@/styles/mixin.scss";

.createPost-container {
  position: relative;

  .createPost-main-container {
    padding: 40px 45px 20px 50px;

    .postInfo-container {
      position: relative;
      @include clearfix;
      margin-bottom: 10px;

      .postInfo-container-item {
        float: left;
      }
    }
  }
}

.article-textarea /deep/ {
  textarea {
    padding-right: 40px;
    resize: none;
    border: none;
    border-radius: 0px;
    border-bottom: 1px solid #bfcbd9;
  }
}
</style>
