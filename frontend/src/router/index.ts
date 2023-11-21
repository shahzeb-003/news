// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios';


// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
    ]
})

export default router;
