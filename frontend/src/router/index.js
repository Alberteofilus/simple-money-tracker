import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import MainWorkspace from '../views/MainWorkspace.vue';
import TransactionForm from '../views/TransactionForm.vue';

const routes = [
    {
        path: '/',
        name: 'login',
        component: Login,
    },
    {
        path: '/workspace',
        name: 'workspace',
        component: MainWorkspace,
    },
    {
        path: '/form/:selectedCategory',
        name: 'TransactionForm',
        component: TransactionForm,
        props: true,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
