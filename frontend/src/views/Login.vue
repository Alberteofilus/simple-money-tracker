<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header text-center">
                        <h3>Login</h3>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="login">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input
                                    v-model="username"
                                    type="text"
                                    class="form-control"
                                    id="username"
                                    placeholder="Enter username"
                                />
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input
                                    v-model="password"
                                    type="password"
                                    class="form-control"
                                    id="password"
                                    placeholder="Enter password"
                                />
                            </div>
                            <button
                                type="submit"
                                class="btn btn-primary btn-block"
                            >
                                Login
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            username: '',
            password: '',
        };
    },
    methods: {
        login() {
            if (this.username === 'user' && this.password === '123456') {
                console.log('Login successful');
                this.$router.push('/workspace');
            } else {
                console.log('Invalid credentials');
            }
        },
    },
};
</script>
