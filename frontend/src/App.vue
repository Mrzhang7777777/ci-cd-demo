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
      throw new Error(`request failed: ${response.status}`);
    }

    const data = (await response.json()) as HelloResponse;
    message.value = data.message;
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : "failed to load backend message";
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
      <p class="eyebrow">frontend</p>
      <h1>ci-cd-demo frontend running</h1>
      <p v-if="loading" class="status-text">loading backend message...</p>
      <p v-else-if="error" class="status-text status-error">error: {{ error }}</p>
      <p v-else class="status-text status-success">{{ message }}</p>
    </section>
  </main>
</template>
