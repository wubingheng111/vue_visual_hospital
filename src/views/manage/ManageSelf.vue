  <template>
      <div class="parent">
        <div class="header">
          <h2>个人信息</h2>
        </div>
        <div class="info-container">
          <table class="info-table">
            <tr>
              <td><strong>姓名:</strong></td>
              <td>{{ person.info.name }}</td>
            </tr>
            <tr>
              <td><strong>用户名:</strong></td>
              <td>{{ person.info.username }}</td>
            </tr>
            <tr>
              <td><strong>密码:</strong></td>
              <td v-if="!person.info.showPassword">******
                <button type="text" size="mini" @click="togglePassword(row)">
              {{ person.info.showPassword ? '隐藏密码' : '显示密码' }}
              </button></td>
              <td v-else>{{ person.info.password }}<button type="text" size="mini" @click="togglePassword(row)">
              {{ person.info.showPassword ? '隐藏密码' : '显示密码' }}
              </button></td>
            </tr>
            <tr>
              <td><strong>性别:</strong></td>
              <td>{{ person.info.gender }}</td>
            </tr>
            <tr>
              <td><strong>联系电话:</strong></td>
              <td>{{ person.info.phone }}</td>
            </tr>
            <tr>
              <td><strong>邮箱地址:</strong></td>
              <td>{{ person.info.email }}</td>
            </tr>
          </table>
        </div>
        <div class="button-container">
          <button @click="handleEdit()">编辑</button>
        </div>

        <el-dialog
          v-model="editDialogVisible"
          title="修改个人信息"
          width="500"
        >
          <el-form :model="editForm"  label-width="80px">
            <el-form-item label="用户名" prop="name">
              <el-input v-model="editForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="price">
              <el-input v-model="editForm.password"></el-input>
            </el-form-item>
            <el-form-item label="联系电话" prop="price">
              <el-input v-model="editForm.phone"></el-input>
            </el-form-item>
            <el-form-item label="邮箱地址" prop="price">
              <el-input v-model="editForm.email"></el-input>
            </el-form-item>
          </el-form>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="closeEditDialog">取消</el-button>
              <el-button type="primary" @click="saveEdit">确定</el-button>
            </div>
          </template>
        </el-dialog>
      </div>
    </template>
    <script setup>
    import { useRouter } from 'vue-router';
    import { useLoginStore } from '@/stores/login';
    import { ref,reactive,onMounted } from 'vue';
    import axios from 'axios';
    const router = useRouter();
    const loginStore = useLoginStore();
    const url = "http://127.0.0.1:8000/api/user/"+loginStore.person125Info.role+"/"+ loginStore.person125Info.id;
    const person = reactive({ info: {} });
    let editDialogVisible = ref(false);

    const editForm = reactive({
      id: null,
      name:'',
      username: '',
      password: '',
      phone:'',
      email:'',
      gender:'',
      role:''
    });

    onMounted(() => {
      fetchData();
    });

    const fetchData = () => {
      axios.get(url).then((response) => {
      person.info = response.data;
      console.log(person.info)
    })
    }
    const togglePassword = () => {
    person.info.showPassword = !person.info.showPassword;
  };
    const handleEdit = (row) => {
      console.log(row);
      editForm.id = person.info.id;
      editForm.name = person.info.name;
      editForm.gender = person.info.gender;
      editForm.username = person.info.username;
      editForm.password = person.info.password;
      editForm.phone = person.info.phone;
      editForm.email = person.info.email;
      console.log(editForm);
      editDialogVisible.value = true; // 设置为 true 以显示编辑对话框
    };

    const closeEditDialog = () => {
      editDialogVisible.value = false; // 关闭编辑对话框
    };

    const saveEdit = () => {
      axios.put("http://127.0.0.1:8000/api/user/"+loginStore.person125Info.role+"/"+loginStore.person125Info.id, {
        role:loginStore.person125Info.role,
        id:loginStore.person125Info.id,
        name:editForm.name,
        gender:editForm.gender,
        username: editForm.username,
        password: editForm.password,
        phone:editForm.phone,
        email:editForm.email
      })
      .then(response => {
        alert("编辑成功！")
        fetchData(); // 重新获取数据更新表格
        closeEditDialog(); // 关闭编辑对话框
        console.log('编辑成功:', response);
      })
      .catch(error => {
        console.error('编辑失败:', error);
      });
    };

    </script>

    <style>
      .parent {
        max-width: 600px;
        margin: 30px auto;
        padding: 20px;
        background-color: #f0f8ff; /* 淡蓝色背景 */
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
      }

      .header {
        text-align: center;
        margin-bottom: 20px;
      }

      .info-container {
        margin-bottom: 20px;
      }

      .info-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #fff; /* 白色背景 */
        border-radius: 5px;
        overflow: hidden;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.1); /* 阴影效果 */
      }

      .info-table td {
        padding: 10px;
        border-bottom: 1px solid #ccc;
      }

      .info-table td:first-child {
        width: 30%;
        font-weight: bold;
      }

      .button-container {
        display: flex;
        justify-content: center;
      }

      .button-container button {
        padding: 10px 20px;
        margin: 0 10px;
        font-size: 16px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }

      .button-container button:hover {
        background-color: #0056b3;
      }
    </style>