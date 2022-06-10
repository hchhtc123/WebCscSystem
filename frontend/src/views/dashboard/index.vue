<template>
  <div class="dashboard-container">
    <el-image
      style="width: 100%; height: 100%;"
      :src="url"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      url: require('/src/assets/img/welcome.png')
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    height:100%;
    width:100%;
    position:fixed;
  }
}
</style>
