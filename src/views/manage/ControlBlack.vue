<template>
  <div class="table-container" style="max-height: 500px; overflow: auto;">
    <el-table :data="currentPageData" border class="centered-table" max-height="500">
      <el-table-column type="index" label="序号" align="center" />
      <el-table-column prop="id" label="用户ID" align="center" />
      <el-table-column prop="name" width="150" label="姓名" align="center" />
      <el-table-column prop="username" width="150" label="用户名" align="center" />
      <el-table-column prop="password" width="150" label="密码" align="center">******</el-table-column>
      <el-table-column prop="gender" label="性别" align="center" />
      <el-table-column prop="email" width="250" label="邮箱" align="center" />
      <el-table-column prop="phone" width="150" label="联系电话" align="center"/>
      <el-table-column label="操作" width="200" align="center">
        <template #default="{ row }">
          <el-button size="small" @click="leaveBlack(index,row)">移除黑名单</el-button>
          <el-button size="small" type="danger" @click="handleDelete(index,row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table><br>

    <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="currentPage"
    :page-sizes="[5, 10, 20]"
    :page-size="pageSize"
    layout="total, sizes, prev, pager, next, jumper"
    :total="total"
  ></el-pagination>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted , computed} from 'vue';
import axios from 'axios';
const showListPicUrl = ref(false); 
const url = 'http://localhost:3000';
const tableData = reactive({ list: [] });
const currentPage = ref(1);
const pageSize = ref(5);
onMounted(() => {
  fetchData();
});

// const fetchData = () => {
//   axios.get(url)
//     .then((response) => {
//       tableData.list = response.data;
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//     });
// };

const fetchData = () => {
axios.get(url, {
  params: {
    status: 0
  }
})
  .then((response) => {
    tableData.list = response.data;
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
};

const total = computed(() => tableData.list.length);
  const currentPageData = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value;
  const endIndex = startIndex + pageSize.value;
  return tableData.list.slice(startIndex, endIndex);
});
const handleSizeChange = (val) => {
  pageSize.value = val;
};

const handleCurrentChange = (val) => {
  currentPage.value = val;
};


const handleDelete = (index,row: { id: string; }) => {
  axios.delete('http://localhost:3000'+row.id)
    .then(response => {
      console.log('删除成功:', response);
      // 从前端移除已删除的数据
      alert("删除成功！");  
      fetchData();
    })
    .catch(error => {
      console.error('删除失败:', error);
    });
};

const leaveBlack = (index, row: { id: string }) => {
axios.get('http://localhost:3000' + row.id)
  .then(response => {
    const user = response.data;

    // 移除拉黑用户
    user.status = '1';

    // 发送修改用户信息的请求
    axios.put('http://localhost:3000' + row.id, user)
      .then(response => {
        console.log('移除拉黑成功:', response);
        // 从前端移除已删除的数据
        alert('移除拉黑成功！');
        fetchData();
      })
      .catch(error => {
        console.error('移除拉黑失败:', error);
      });
  })
  .catch(error => {
    console.error('用户查找失败:', error);
  });
};

</script>


<style scoped> 
.centered-table {
  width: 100%;
  margin-top: 20px;
}

.el-table th,
.el-table td {
  text-align: center;
}

</style>