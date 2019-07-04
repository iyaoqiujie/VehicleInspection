<template>
  <el-form>
    <el-form-item label="用户编号">
      <el-input v-model.trim="user.userId" />
    </el-form-item>
    <el-form-item label="用户名">
      <el-input v-model.trim="user.username" />
    </el-form-item>
    <el-form-item label="手机号">
      <el-input v-model.trim="user.mobile" />
    </el-form-item>
    <el-form-item label="电子邮件">
      <el-input v-model.trim="user.email" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">提交更新</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { updateUser } from '@/api/user'

export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          userId: undefined,
          username: '',
          mobile: '',
          email: '',
          id_card: ''
        }
      }
    }
  },
  methods: {
    submit() {
      const userInfo = {
        email: this.user.email
      }
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        updateUser(this.user.userId, userInfo).then(() => {
          this.$notify({
            title: '成功',
            message: '修改用户信息成功',
            type: 'success',
            duration: 1000
          })
        }).catch(error => {
          console.log('rejected: ', error)
          this.$message({
            message: '修改用户信息失败',
            type: 'error'
          })
        })
      })
    }
  }
}
</script>
