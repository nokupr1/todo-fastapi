<script setup>
import { ref, onMounted, computed } from "vue";

const tasks = ref([]);
const newTaskName = ref("");
const newTaskDesc = ref("");
const filter = ref("all");
const isDark = ref(false);

const API_URL = "http://localhost:8000/api/tasks";

const toggleTheme = () => {
    isDark.value = !isDark.value;
    if (isDark.value) {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark");
    } else {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light");
    }
};

const fetchTasks = async () => {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();
        tasks.value = data.tasks || [];
    } catch (error) {
        console.error("Ошибка при загрузке задач:", error);
    }
};

const addTask = async () => {
    if (!newTaskName.value.trim()) return;

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: newTaskName.value,
                description: newTaskDesc.value,
                is_done: false,
            }),
        });
        if (res.ok) {
            newTaskName.value = "";
            newTaskDesc.value = "";
            fetchTasks();
        }
    } catch (error) {
        console.error("Ошибка при создании задачи:", error);
    }
};

const toggleTask = async (task) => {
    try {
        const res = await fetch(`${API_URL}/${task.id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ is_done: !task.is_done }),
        });
        if (res.ok) fetchTasks();
    } catch (error) {
        console.error("Ошибка при обновлении статуса:", error);
    }
};

const deleteTask = async (id) => {
    try {
        const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        if (res.ok) fetchTasks();
    } catch (error) {
        console.error("Ошибка при удалении:", error);
    }
};

const filteredTasks = computed(() => {
    let result = tasks.value;
    if (filter.value === "active")
        result = tasks.value.filter((t) => !t.is_done);
    else if (filter.value === "completed")
        result = tasks.value.filter((t) => t.is_done);

    return [...result].sort((a, b) => {
        if (a.is_done === b.is_done) return b.id - a.id;
        return a.is_done ? 1 : -1;
    });
});

onMounted(() => {
    fetchTasks();
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)",
    ).matches;

    if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
        isDark.value = true;
        document.documentElement.classList.add("dark");
    }
});
</script>

<template>
    <div
        class="min-h-screen flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
    >
        <div class="w-full max-w-3xl">
            <div class="relative w-full flex items-center justify-center mb-12">
                <h1
                    class="text-5xl font-extrabold text-center text-primary tracking-tight"
                >
                    QuickDo
                </h1>

                <button
                    @click="toggleTheme"
                    class="absolute right-0 w-16 h-8 rounded-full bg-surface border-2 border-secondary/50 transition-all duration-300 outline-none focus-visible:ring-4 focus-visible:ring-primary/20 flex items-center px-1 hover:border-primary/50 cursor-pointer"
                    title="Сменить тему"
                >
                    <div
                        class="flex items-center justify-center w-6 h-6 rounded-full bg-background border border-secondary/30 shadow-sm transform transition-transform duration-300"
                        :class="isDark ? 'translate-x-7' : 'translate-x-0'"
                    >
                        <svg
                            v-if="!isDark"
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-3.5 w-3.5 text-primary"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 4.22a1 1 0 011.415 0l.884.884a1 1 0 01-1.414 1.415l-.884-.884a1 1 0 010-1.415zM1 10a1 1 0 011-1h1a1 1 0 110 2H2a1 1 0 01-1-1zm15 0a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1zM5.636 15.778a1 1 0 010-1.414l.884-.884a1 1 0 011.415 1.414l-.884.884a1 1 0 01-1.415 0zM14.364 4.222a1 1 0 010 1.414l-.884.884a1 1 0 01-1.415-1.414l.884-.884a1 1 0 011.415 0zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm-4.22-4.22a1 1 0 010-1.415l-.884-.884a1 1 0 011.414-1.415l.884.884a1 1 0 01-1.415 1.415zM10 5a5 5 0 100 10 5 5 0 000-10z"
                                clip-rule="evenodd"
                            />
                        </svg>
                        <svg
                            v-else
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-3.5 w-3.5 text-primary"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                        >
                            <path
                                d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"
                            />
                        </svg>
                    </div>
                </button>
            </div>

            <div
                class="bg-surface p-6 rounded-2xl shadow-sm border border-secondary/40 mb-8 transition-colors duration-500"
            >
                <div class="flex flex-col sm:flex-row gap-4">
                    <div class="flex-1 space-y-3">
                        <input
                            v-model="newTaskName"
                            @keyup.enter="addTask"
                            type="text"
                            placeholder="Что нужно сделать?"
                            class="w-full px-4 py-3 border border-secondary/50 rounded-xl outline-none focus:outline-none focus-visible:outline-none focus:border-primary focus:ring-2 focus:ring-primary/40 transition-all text-text placeholder-text/40 bg-background appearance-none"
                        />
                        <input
                            v-model="newTaskDesc"
                            @keyup.enter="addTask"
                            type="text"
                            placeholder="Дополнительное описание (необязательно)"
                            class="w-full px-4 py-2 border border-secondary/30 rounded-xl text-sm outline-none focus:outline-none focus-visible:outline-none focus:border-primary focus:ring-2 focus:ring-primary/40 transition-all text-text placeholder-text/40 bg-background appearance-none"
                        />
                    </div>
                    <button
                        @click="addTask"
                        class="bg-primary hover:bg-accent text-white font-semibold py-3 px-8 rounded-xl transition-all shadow-md shadow-primary/20 active:scale-95 h-fit sm:h-auto whitespace-nowrap outline-none focus-visible:ring-4 focus-visible:ring-primary/30"
                    >
                        Добавить
                    </button>
                </div>
            </div>

            <div class="flex justify-center space-x-2 mb-8">
                <button
                    @click="filter = 'all'"
                    :class="[
                        'px-5 py-2 rounded-full text-sm font-semibold transition-all outline-none focus-visible:ring-2 focus-visible:ring-primary/50',
                        filter === 'all'
                            ? 'bg-primary text-white shadow-md shadow-primary/20'
                            : 'bg-surface text-text/70 hover:bg-secondary/20 border border-secondary/30',
                    ]"
                >
                    Все
                </button>
                <button
                    @click="filter = 'active'"
                    :class="[
                        'px-5 py-2 rounded-full text-sm font-semibold transition-all outline-none focus-visible:ring-2 focus-visible:ring-primary/50',
                        filter === 'active'
                            ? 'bg-primary text-white shadow-md shadow-primary/20'
                            : 'bg-surface text-text/70 hover:bg-secondary/20 border border-secondary/30',
                    ]"
                >
                    В процессе
                </button>
                <button
                    @click="filter = 'completed'"
                    :class="[
                        'px-5 py-2 rounded-full text-sm font-semibold transition-all outline-none focus-visible:ring-2 focus-visible:ring-primary/50',
                        filter === 'completed'
                            ? 'bg-primary text-white shadow-md shadow-primary/20'
                            : 'bg-surface text-text/70 hover:bg-secondary/20 border border-secondary/30',
                    ]"
                >
                    Выполненные
                </button>
            </div>

            <div class="space-y-4">
                <div
                    v-if="filteredTasks.length === 0"
                    class="text-center py-12 text-text/50 font-medium text-lg transition-colors duration-500"
                >
                    Задач пока нет. Отличное время, чтобы добавить новую! 🌱
                </div>

                <div
                    v-for="task in filteredTasks"
                    :key="task.id"
                    class="bg-surface p-5 rounded-2xl shadow-sm border border-secondary/30 flex items-start gap-4 transition-all duration-500 hover:shadow-md hover:border-primary/40 group"
                    :class="{ 'opacity-60 bg-background/50': task.is_done }"
                >
                    <div class="pt-1 relative">
                        <input
                            type="checkbox"
                            :checked="task.is_done"
                            @change="toggleTask(task)"
                            class="w-6 h-6 text-primary rounded-md border-2 border-secondary/50 focus:ring-4 focus:ring-primary/20 focus:ring-offset-0 focus:outline-none cursor-pointer transition-all bg-background accent-primary"
                        />
                    </div>

                    <div class="flex-1 min-w-0">
                        <h3
                            class="text-lg font-semibold text-text truncate transition-all duration-300"
                            :class="{
                                'line-through text-text/40': task.is_done,
                            }"
                        >
                            {{ task.name }}
                        </h3>
                        <p
                            v-if="task.description"
                            class="text-text/60 text-sm mt-1 leading-relaxed transition-all duration-300"
                            :class="{
                                'line-through text-text/30': task.is_done,
                            }"
                        >
                            {{ task.description }}
                        </p>
                    </div>

                    <button
                        @click="deleteTask(task.id)"
                        class="text-text/30 hover:text-red-500 transition-colors p-2 rounded-xl hover:bg-red-500/10 opacity-0 group-hover:opacity-100 outline-none focus:opacity-100 focus-visible:ring-2 focus-visible:ring-red-500/30"
                        title="Удалить задачу"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
