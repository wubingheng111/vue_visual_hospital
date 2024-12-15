<template>
  <el-button size="small" @click="AddUser">添加用户</el-button>
  <div class="table-container">
    <el-table :data="currentPageData" border class="centered-table" max-height="500">
      <el-table-column type="index" label="序号" align="center" />
      <el-table-column prop="id" label="用户ID" align="center" />
      <el-table-column prop="name" width="150" label="姓名" align="center" />
      <el-table-column prop="username" width="150" label="用户名" align="center" />
      <el-table-column prop="password" width="100" label="密码" align="center">******</el-table-column>
      <el-table-column prop="gender" label="性别" align="center" />
      <el-table-column prop="email" width="250" label="邮箱" align="center" />
      <el-table-column prop="phone" width="150" label="联系电话" align="center"/>
      <el-table-column label="操作" width="250" align="center">
        <template #default="{ row }">
          <el-button size="small" @click="toBlack(index,row)">拉黑</el-button>
          <el-button size="small" @click="handleEdit(index,row)">重置密码</el-button>
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

    <el-dialog
      v-model="editDialogVisible1"
      title="添加用户信息"
      width="500"
    >
      <el-form :model="addForm"  label-width="80px">
        <el-form-item label="姓名" prop="title">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="content">
          <el-select id="gender" v-model="addForm.gender" required>
          <el-option value="male">男</el-option>
          <el-option value="female">女</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用户名" prop="image_url">
          <el-input v-model="addForm.username"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="image_url">
          <el-input v-model="addForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="image_url">
          <el-input v-model="addForm.email"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeEditDialog1">取消</el-button>
          <el-button type="primary" @click="saveAdd">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';
const showListPicUrl = ref(false); 
const url = 'http://localhost:3000/user';
const tableData1 = reactive({ list: [] });
const tableData = reactive({ list: [] });
let editDialogVisible1 = ref(false);
const currentPage = ref(1);
const pageSize = ref(5);

onMounted(() => {
  fetchData();
});

const fetchData = () => {
axios.get(url, {
  params: {
    status: 1
  }
})
  .then((response) => {
    tableData1.list = response.data;
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
};

//分页
const total = computed(() => tableData1.list.length);
  const currentPageData = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value;
  const endIndex = startIndex + pageSize.value;
  return tableData1.list.slice(startIndex, endIndex);
});

const handleSizeChange = (val) => {
  pageSize.value = val;
};

const handleCurrentChange = (val) => {
  currentPage.value = val;
};

//增加用户
let addForm = reactive({
    id:null,
    role: "user",
    name: '',
    gender: '',
    username:'',
    password:'123456',
    phone:'',
    email:'',
    status:'1',
  });

  const AddUser = () => {
    editDialogVisible1.value = true; // 设置为 true 以显示添加对话框
  };
  const closeEditDialog1 = () => {
    editDialogVisible1.value = false; // 关闭添加对话框
  };
  const saveAdd = () => {
    axios.get(url)
    .then((response) => {
      let userData = response.data;
      // 确定最大的 id 值，如果用户列表为空，则设置 maxId 为 0
      let maxId = userData.length > 0 ? Math.max(...userData.map(user => user.id)) : 0;
      // 设置用户的 id 为最大id值加一
      addForm.id = `${maxId + 1}`;

      // 发送 POST 请求保存新用户
      return axios.post(url, addForm);
    })
    .then(response => {
      console.log('保存成功:', response.data);
      alert("添加成功！");

      // 获取最新的用户数据并更新本地数据
      return axios.get(url);
    })
    .then(response => {
      tableData.list = response.data;
      editDialogVisible1.value = false;
      fetchData();
      // 清空 addForm，准备下一次添加
      Object.assign(addForm, {
        id: null,
        role: "user",
        name: '',
        gender: '',
        username: '',
        password: '123456',
        phone: '',
        email: '',
        status: '1',
      });
    })
    .catch(error => {
      console.error('保存失败:', error);
    });
};

//删除用户
const handleDelete = (index,row: { id: string; }) => {
  axios.delete('http://localhost:3000/user/'+row.id)
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

//修改用户
const handleEdit = (index, row: { id: string }) => {
axios.get('http://localhost:3000/user/' + row.id)
  .then(response => {
    const user = response.data;

    // 修改用户的密码
    user.password = '123456';

    // 发送修改用户信息的请求
    axios.put('http://localhost:3000/user/' + row.id, user)
      .then(response => {
        console.log('密码重置成功:', response);
        // 从前端移除已删除的数据
        alert('密码重置成功！');
        fetchData();
      })
      .catch(error => {
        console.error('密码重置失败:', error);
      });
  })
  .catch(error => {
    console.error('用户查找失败:', error);
  });
};

//拉黑用户
const toBlack = (index, row: { id: string }) => {
axios.get('http://localhost:3000/user/' + row.id)
  .then(response => {
    const user = response.data;
    // 拉黑用户
    user.status = '0';
    // 发送修改用户信息的请求
    axios.put('http://localhost:3000/user/' + row.id, user)
      .then(response => {
        console.log('拉黑成功:', response);
        // 从前端移除已删除的数据
        alert('拉黑用户成功！');
        fetchData();
      })
      .catch(error => {
        console.error('拉黑失败:', error);
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