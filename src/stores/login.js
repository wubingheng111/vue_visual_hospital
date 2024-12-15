import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useLoginStore = defineStore('myinfo', () => 
{
  const person125Info = ref({
    id:'',
    name:'',
    role:'',
    status:'',
    state:true
  })

  return { person125Info }
  },
  {
    persist: true,
  }
)
  