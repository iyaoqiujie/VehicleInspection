<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">

      <sticky :z-index="10" :class-name="'sub-navbar '+postForm.status">
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          修改
        </el-button>
      </sticky>

      <div class="createPost-main-container">
        <el-row>
          <el-col :span="18">
            <el-form-item style="margin-bottom: 40px;" prop="name">
              <MDinput v-model="postForm.name" :maxlength="100" name="name" required readonly>
                检测点名称
              </MDinput>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="18">
            <el-form-item style="margin-bottom: 40px;" prop="address">
              <MDinput v-model="postForm.address" :maxlength="100" name="address" required>
                检测点地址
              </MDinput>
            </el-form-item>
          </el-col>
        </el-row>

        <div class="postInfo-container">
          <el-row :gutter="40">
            <el-col :span="10">
              <el-form-item style="margin-bottom: 40px;" prop="contact">
                <MDinput v-model="postForm.contact" :maxlength="80" name="contact">
                  联系人姓名
                </MDinput>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item style="margin-bottom: 40px;" prop="phone">
                <MDinput v-model="postForm.phone" :maxlength="80" name="phone">
                  联系人电话
                </MDinput>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <el-row>
          <el-col :span="18">
            <el-form-item  style="margin-bottom: 40px;" label-width="100px" label="检测点管理员:">
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
import { fetchStation, updateStation } from '@/api/station'

export default {
  name: 'StationDetail',
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
        id: undefined,
        name: '',
        address: '',
        contact: '',
        phone: '',
        stationadmin: ''
      },
      stationAdminInfo: '',
      loading: false,
      rules: {
      }
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
      fetchStation().then(response => {
        if (response.name) {
          this.postForm.id = response.id
          this.postForm.name = response.name
          this.postForm.address = response.address
          this.postForm.contact = response.contact
          this.postForm.phone = response.phone
          this.postForm.stationadmin = response.admin_username
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
            updateStation(this.postForm.id, this.postForm).then(() => {
              this.loading = false
              this.$notify({
                title: '成功',
                message: '修改检测站信息成功',
                type: 'success',
                duration: 1000
              })
              this.fetchData()
            }).catch(error => {
              console.log('rejected: ', error)
              this.loading = false
              this.$message({
                message: '创建预约订单失败',
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
