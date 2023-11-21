<template>
    <main class="container pt-4">
        <div>
            <router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Profile Page'}"
            >
                Profile Page
            </router-link>
        </div>
        <RouterView/>
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>

<style scoped>
</style>
