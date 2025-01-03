<template>
    <div class="money-tracker-container">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
            <div class="container">
                <a class="navbar-brand" href="/workspace">
                    <i class="fas fa-chart-line mr-2"></i>Money Tracker
                </a>
                <button 
                    class="navbar-toggler" 
                    type="button" 
                    data-toggle="collapse" 
                    data-target="#navbarText"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarText">
                    <ul class="navbar-nav mr-auto">
                    </ul>
                    <span class="navbar-text">
                        <button class="btn btn-outline-light" @click="logout">
                            <i class="fas fa-sign-out-alt mr-2"></i>Logout
                        </button>
                    </span>
                </div>
            </div>
        </nav>

        <div class="container py-4">
            <div class="card shadow-sm">
                <div class="card-header bg-light">
                    <h5 class="mb-0">
                        <i class="fas fa-plus mr-2"></i>Add New Transaction
                    </h5>
                </div>
                <div class="card-body">
                    <form @submit.prevent="submitForm">
                        <div class="form-group">
                            <label for="date" class="font-weight-bold">
                                <i class="fas fa-calendar-alt mr-2"></i>Date
                            </label>
                            <input
                                type="date"
                                id="date"
                                v-model="date"
                                class="form-control"
                                required
                            />
                        </div>
                        <div class="form-group">
                            <label for="amount" class="font-weight-bold">
                                <i class="fas fa-dollar-sign mr-2"></i>Amount
                            </label>
                            <input
                                type="number"
                                id="amount"
                                v-model="amount"
                                class="form-control"
                                required
                            />
                        </div>
                        <div class="form-group">
                            <label for="category" class="font-weight-bold">
                                <i class="fas fa-tag mr-2"></i>Category
                            </label>
                            <input
                                type="text"
                                id="category"
                                :value="selectedCategory"
                                class="form-control"
                                readonly
                            />
                        </div>
                        <div class="form-group">
                            <label for="description" class="font-weight-bold">
                                <i class="fas fa-comment-dots mr-2"></i>Description
                            </label>
                            <textarea
                                id="description"
                                v-model="description"
                                class="form-control"
                                required
                            ></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-plus mr-2"></i>Add Transaction
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>
.money-tracker-container {
    background-color: #f4f6f9;
    min-height: 100vh;
}

.card {
    max-width: 600px;
    border-radius: 10px;
    margin: 0 auto;
}

.form-group {
    margin-bottom: 1.5rem;
}

.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #004a9b;
}
</style>

<script>
import axios from 'axios';

export default {
    props: ['selectedCategory'],
    data() {
        return {
            date: '',
            amount: '',
            description: '',
        };
    },
    methods: {
        submitForm() {
            const newTransaction = {
                date: this.date,
                amount: this.amount,
                category: this.selectedCategory,
                description: this.description,
            };
            axios
                .post('http://127.0.0.1:5000/api/transactions', newTransaction)
                .then(() => {
                    this.$router.push('/workspace');
                })
                .catch((error) => {
                    console.error('Error adding transaction:', error);
                });
        },
        logout() {
            this.$router.push('/');
        },
    },
};
</script>