<script setup lang="ts">
import { onMounted, ref } from "vue";

type HelloResponse = {
  message: string;
};

const message = ref<string>("");
const loading = ref<boolean>(true);
const error = ref<string>("");

async function loadHello(): Promise<void> {
  loading.value = true;
  error.value = "";

  try {
    const response = await fetch("/api/hello");

    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`);
    }

    const data = (await response.json()) as HelloResponse;
    message.value = data.message;
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : "无法连接后端服务";
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  void loadHello();
});
</script>

<template>
  <main class="app-shell">
    <section class="card">
      <p class="eyebrow">CI/CD 演示项目</p>
      <h1>自动化部署已就绪</h1>
      <p v-if="loading" class="status-text">正在连接后端服务...</p>
      <p v-else-if="error" class="status-text status-error">错误：{{ error }}</p>
      <p v-else class="status-text status-success">后端响应：{{ message }}</p>
    </section>
  </main>
</template>
