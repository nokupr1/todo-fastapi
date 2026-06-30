<script setup>
import { ref, onMounted, computed } from 'vue'

const tasks = ref([])
const newTaskName = ref('')
const newTaskDesc = ref('')
const filter = ref('all') // 'all', 'active', 'completed'

const API_URL = 'http://localhost:8000/api/tasks'

// Получение всех задач
const fetchTasks = async () => {
  try {
    const res = await fetch(API_URL)
    const data = await res.json()
    tasks.value = data.tasks || []
  } catch (error) {
    console.error('Ошибка при загрузке задач:', error)
  }
}

// Добавление новой задачи
const addTask = async () => {
  if (!newTaskName.value.trim()) return

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newTaskName.value,
        description: newTaskDesc.value,
        is_done: false
      })
    })

    if (res.ok) {
      newTaskName.value = ''
      newTaskDesc.value = ''
      fetchTasks()
    }
  } catch (error) {
    console.error('Ошибка при создании задачи:', error)
  }
}

// Изменение статуса задачи (PATCH)
const toggleTask = async (task) => {
  try {
    const res = await fetch(`${API_URL}/${task.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_done: !task.is_done })
    })

    if (res.ok) fetchTasks()
  } catch (error) {
    console.error('Ошибка при обновлении статуса:', error)
  }
}

// Удаление задачи
const deleteTask = async (id) => {
  try {
    const res = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE'
    })

    if (res.ok) fetchTasks()
  } catch (error) {
    console.error('Ошибка при удалении:', error)
  }
}

// Фильтрация задач для отображения
const filteredTasks = computed(() => {
  if (filter.value === 'active') return tasks.value.filter(t => !t.is_done)
  if (filter.value === 'completed') return tasks.value.filter(t => t.is_done)
  return tasks.value
})

onMounted(fetchTasks)
</script>

<template>
  <div class="min-h-screen py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">

      <h1 class="text-3xl font-bold text-center text-indigo-600 mb-8">📝 Мои задачи</h1>

      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="flex-1 space-y-3">
            <input
              v-model="newTaskName"
              @keyup.enter="addTask"
              type="text"
              placeholder="Что нужно сделать?"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
            />
            <input
              v-model="newTaskDesc"
              @keyup.enter="addTask"
              type="text"
              placeholder="Дополнительное описание (необязательно)"
              class="w-full px-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
            />
          </div>
          <button
            @click="addTask"
            class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-6 rounded-lg transition-colors h-fit sm:h-auto"
          >
            Добавить
          </button>
        </div>
      </div>

      <div class="flex justify-center space-x-2 mb-6">
        <button @click="filter = 'all'" :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-colors', filter === 'all' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100']">Все</button>
        <button @click="filter = 'active'" :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-colors', filter === 'active' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100']">В процессе</button>
        <button @click="filter = 'completed'" :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-colors', filter === 'completed' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100']">Выполненные</button>
      </div>

      <div class="space-y-3">
        <div v-if="filteredTasks.length === 0" class="text-center py-10 text-gray-500">
          Задач пока нет. Отличное время, чтобы добавить новую! 🎉
        </div>

        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-start gap-4 transition-all hover:shadow-md"
          :class="{'opacity-75 bg-gray-50': task.is_done}"
        >
          <div class="pt-1">
            <input
              type="checkbox"
              :checked="task.is_done"
              @change="toggleTask(task)"
              class="w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer transition-all"
            >
          </div>

          <div class="flex-1 min-w-0">
            <h3
              class="text-lg font-medium text-gray-900 truncate transition-all"
              :class="{'line-through text-gray-400': task.is_done}"
            >
              {{ task.name }}
            </h3>
            <p v-if="task.description" class="text-gray-500 text-sm mt-1" :class="{'line-through text-gray-400': task.is_done}">
              {{ task.description }}
            </p>
          </div>

          <button
            @click="deleteTask(task.id)"
            class="text-gray-400 hover:text-red-500 transition-colors p-1 rounded-md hover:bg-red-50"
            title="Удалить задачу"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

    </div>
  </div>
</template>
