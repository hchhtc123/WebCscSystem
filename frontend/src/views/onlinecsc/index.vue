<template>
  <div class="app-container">
    <div class="tip">
      请输入要进行纠错的文本:
    </div>
    <el-input v-model="textarea" type="textarea" :disabled="stage" :rows="11" placeholder="请输入要进行纠错的文本" clearable />

    <div style="text-align: center; padding-top:10px;padding-bottom:10px;">
      <el-upload
        ref="upload"
        action="/"
        accept=".txt"
        :before-upload="beforeUpload"
        :show-file-list="false"
        :default-file-list="fileList"
      >
        <el-button slot="trigger" type="primary" round style="margin-left:10px;margin-right:10px;">导入txt</el-button>
        <el-button type="info" round style="margin-left:10px;margin-right:10px;" @click="clear()">清空</el-button>
        <el-button type="success" round @click="errorCorrect()">纠错</el-button>
        <el-button type="primary" round @click="saveResult()">保存结果</el-button>
      </el-upload>
    </div>

    <div v-show="visible" class="tip">
      文本纠错结果:
    </div>
    <el-input v-show="visible" v-model="result" type="textarea" :rows="11" />

  </div>
</template>

<script>
import axios from 'axios'
import { saveAs } from 'file-saver'
export default {
  data() {
    return {
      textarea: '',
      result: '',
      stage: false,
      visible: false,
      fileList: ''
    }
  },
  beforeCreate() {
    // 读取文件
    FileReader.prototype.reading = function({ encode } = 'pms') {
      const bytes = new Uint8Array(this.result) // 无符号整型数组
      const text = new TextDecoder(encode || 'UTF-8').decode(bytes)
      return text
    }
    /* 重写readAsBinaryString函数 */
    FileReader.prototype.readAsBinaryString = function(f) {
      // 如果this未重写onload函数，则创建一个公共处理方式
      if (!this.onload) {
        this.onload = e => { // 在this.onload函数中，完成公共处理
          const rs = this.reading()
          console.log(rs)
        }
      }
      this.readAsArrayBuffer(f) // 内部会回调this.onload方法
    }
  },
  methods: {
    clear() {
      var that = this
      that.textarea = ''
      that.result = ''
      that.visible = false
      that.$message({
        showClose: true,
        message: '文本内容已清空！',
        type: 'success'
      })
    },
    errorCorrect() {
      var that = this
      var context = that.textarea
      if (context === '') {
        this.$message({
          showClose: true,
          message: '输入文本内容不能为空',
          type: 'warning'
        })
        that.result = ''
        that.visible = false
      } else {
        // 请求后端API服务，请求方法为post，请求体字段为json格式 text
        axios.post('http://127.0.0.1:8000/v1/textCorrect', {
          text: that.textarea
        }).then((response) => {
          console.log(response.data)
          that.result = response.data.correctionResults
          that.visible = true
          that.$message({
            showClose: true,
            message: '文本纠错完成！',
            type: 'success'
          })
        }).catch((error) => {
          console.log(error)
          that.result = ''
          that.visible = false
          that.$message({
            showClose: true,
            message: '请求出现异常！',
            type: 'error'
          })
        })
      }
    },
    beforeUpload(file) {
      this.fileList = [file]
      // 读取txt文件
      this.read(file)
      this.$message({
        showClose: true,
        message: 'txt文本内容导入成功！',
        type: 'success'
      })
      return false
    },
    read(f) {
      const rd = new FileReader()
      var that = this
      rd.onload = e => {
      // this.readAsArrayBuffer函数内，会回调this.onload函数。在这里处理结果
        const cont = rd.reading({ encode: 'UTF-8' })
        console.log(cont)
        that.textarea = cont
      }
      rd.readAsBinaryString(f)
    },
    saveResult() {
      var tempData = this.result
      if (tempData === '') {
        this.$message({
          showClose: true,
          message: '纠错结果内容为空！',
          type: 'warning'
        })
      } else {
        var tempResult = new Blob([tempData], { type: 'text/plain;charset=utf-8' })
        saveAs(tempResult, '文本纠错结果.txt')
      }
    }
  }
}
</script>

<style scoped>
  .tip {
    font-family: 宋体;
	font-size: 18px;
	font-weight: bold;
	margin-bottom: 10px;
  }
</style>
