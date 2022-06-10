<template>
  <div class="app-container">
    <div class="tip">
      请上传要进行纠错的图片文件
    </div>
    <el-upload
      class="upload-demo"
      drag
      action=""
      :limit="1"
      :http-request="uploadImg"
      accept=".jpg,.jpeg,.png,.bmp"
      style="text-align: center; padding-top:10px;padding-bottom:10px;"
    >
      <i class="el-icon-upload" />
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
    <el-row style="text-align: center; padding-top:10px;padding-bottom:30px;">
      <el-button type="success" round @click="imageCorrect()">图片纠错</el-button>
      <el-button type="primary" round @click="saveResult()">保存结果</el-button>
    </el-row>
    <div v-show="visible" class="tip">
      图片识别和纠错结果：
    </div>
    <el-input v-show="visible" v-model="imgCscResult" type="textarea" :rows="12" />
  </div>
</template>

<script>
import axios from 'axios'
import { saveAs } from 'file-saver'
export default {
  data() {
    return {
      fileData: '',
      imgCscResult: '',
      visible: false
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
    // 储存选择的file文件
    uploadImg(file) {
      this.fileData = file.file
      console.log(file.file)
      this.$message({
        showClose: true,
        message: '图片上传成功！',
        type: 'success'
      })
    },
    // 保存纠错结果
    saveResult() {
      // console.log(this.fileList)
      var tempData = this.imgCscResult
      if (tempData === '') {
        this.$message({
          showClose: true,
          message: '纠错结果内容为空！',
          type: 'warning'
        })
      } else {
        var tempResult = new Blob([tempData], { type: 'text/plain;charset=utf-8' })
        saveAs(tempResult, '图片纠错结果.txt')
      }
    },
    imageCorrect() {
      var that = this
      if (that.fileData === '') {
        this.$message({
          showClose: true,
          message: '请先选择要进行纠错的图片文件！',
          type: 'warning'
        })
        that.imgCscResult = ''
        that.visible = false
        return
      }
      var config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      var form = new FormData()
      form.append('file', that.fileData)
      // 请求后端API服务，请求方法为post
      axios.post('http://127.0.0.1:8000/v1/imageCorrect', form, config).then((response) => {
        that.imgCscResult = response.data.correctionResults
        that.visible = true
        that.$message({
          showClose: true,
          message: '图片纠错完成！',
          type: 'success'
        })
      }).catch((error) => {
        console.log(error)
        that.imgCscResult = ''
        that.visible = false
        that.$message({
          showClose: true,
          message: '请求出现异常！',
          type: 'error'
        })
      })
    }
  }
}

</script>

<style scoped>
  .tip {
    font-family: 宋体;
  font-size: 18px;
	font-weight: bold;
	margin-bottom: 20px;
  margin-bottom: 10px;
  text-align: center;
  }
</style>
