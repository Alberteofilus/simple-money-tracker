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
                    <ul class="navbar-nav mr-auto"></ul>
                    <span class="navbar-text">
                        <button class="btn btn-outline-light" @click="logout">
                            <i class="fas fa-sign-out-alt mr-2"></i>Logout
                        </button>
                    </span>
                </div>
            </div>
        </nav>

        <div class="container py-4">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">
                        <i class="fas fa-filter mr-2"></i>Filters
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <div class="form-group">
                                <label for="date-range" class="font-weight-bold">Date Range</label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text">
                                            <i class="fas fa-calendar-alt"></i>
                                        </span>
                                    </div>
                                    <input
                                        type="date"
                                        id="date-range-start"
                                        v-model="dateRangeStart"
                                        class="form-control"
                                    />
                                    <div class="input-group-prepend input-group-append">
                                        <span class="input-group-text">to</span>
                                    </div>
                                    <input
                                        type="date"
                                        id="date-range-end"
                                        v-model="dateRangeEnd"
                                        class="form-control"
                                    />
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 mb-3">
                            <div class="form-group">
                                <label class="font-weight-bold mb-2">Categories</label>
                                <div class="d-flex flex-wrap justify-content-center">
                                    <div
                                        v-for="category in categories"
                                        :key="category"
                                        class="custom-control custom-checkbox mr-3 mb-2"
                                    >
                                        <input
                                            type="checkbox"
                                            class="custom-control-input"
                                            :id="category"
                                            :value="category"
                                            v-model="selectedCategories"
                                        />
                                        <label 
                                            class="custom-control-label" 
                                            :for="category"
                                        >
                                            {{ category }}
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">
                        <i class="fas fa-dollar-sign mr-2"></i>Budget Limits
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div 
                            v-for="category in categories" 
                            :key="category" 
                            class="col-md-4 mb-3"
                        >
                            <div class="form-group">
                                <label :for="'budget-' + category">
                                    Category {{ category }} Limit
                                </label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text">IDR</span>
                                    </div>
                                    <input 
                                        :id="'budget-' + category"
                                        type="number" 
                                        class="form-control"
                                        v-model.number="budgetByCategory[category]"
                                        @change="updateBudgetLimit(category)"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div 
                v-if="selectedCategories.length > 0" 
                class="card shadow-sm"
            >
                <div class="card-header bg-light d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                        <i class="fas fa-list mr-2"></i>Transactions
                    </h5>
                    <small class="text-muted">
                    </small>
                </div>
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead class="thead-light">
                            <tr>
                                <th>Date</th>
                                <th 
                                    v-for="category in selectedCategories" 
                                    :key="category"
                                    class="text-center"
                                >
                                    {{ category }}
                                    <button
                                        class="btn btn-sm btn-success ml-2"
                                        @click="navigateToTransactionForm(category)"
                                    >
                                        <i class="fas fa-plus"></i>
                                    </button>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr 
                                v-for="transactionGroup in filteredTransactions" 
                                :key="transactionGroup.date"
                            >
                                <td>{{ transactionGroup.date }}</td> 
                                <td
                                    v-for="category in selectedCategories"
                                    :key="category"
                                    :class="{
                                        'table-danger': 
                                            transactionGroup[category] && 
                                            totalAmount(category) > budgetByCategory[category]
                                    }"
                                >
                                    <TransactionCard
                                        v-if="transactionGroup[category]"
                                        :transaction="transactionGroup[category]"
                                        @edit-transaction="openEditModal"
                                    />
                                    <span v-else>-</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div 
                v-if="showEditModal" 
                class="modal fade show" 
                tabindex="-1" 
                style="display: block;"
            >
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content shadow">
                        <div class="modal-header bg-light">
                            <h5 class="modal-title">
                                <i class="fas fa-edit mr-2"></i>Edit Transaction
                            </h5>
                            <button
                                type="button"
                                class="close text-danger"
                                @click="closeEditModal"
                                aria-label="Close"
                            >
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="updateTransaction">
                                <div class="form-group">
                                    <label for="edit-date">
                                        <i class="fas fa-calendar mr-2"></i>Date
                                    </label>
                                    <input
                                        type="date"
                                        id="edit-date"
                                        v-model="currentTransaction.date"
                                        class="form-control"
                                        required
                                    />
                                </div>
                                <div class="form-group">
                                    <label for="edit-amount">
                                        <i class="fas fa-dollar-sign mr-2"></i>Amount
                                    </label>
                                    <input
                                        type="number"
                                        id="edit-amount"
                                        v-model.number="currentTransaction.amount"
                                        class="form-control"
                                        required
                                    />
                                </div>
                                <div class="form-group">
                                    <label for="edit-description">
                                        <i class="fas fa-comment-dots mr-2"></i>Description
                                    </label>
                                    <textarea
                                        id="edit-description"
                                        v-model="currentTransaction.description"
                                        class="form-control"
                                        required
                                    ></textarea>
                                </div>
                                <div class="form-group">
                                    <label for="edit-category">
                                        <i class="fas fa-tag mr-2"></i>Category
                                    </label>
                                    <select
                                        id="edit-category"
                                        v-model="currentTransaction.category"
                                        class="form-control"
                                        required
                                    >
                                        <option 
                                            v-for="category in categories" 
                                            :key="category" 
                                            :value="category"
                                        >
                                            Category {{ category }}
                                        </option>
                                    </select>
                                </div>
                                <div class="modal-footer">
                                    <button
                                        type="submit"
                                        class="btn btn-primary"
                                    >
                                        <i class="fas fa-save mr-2"></i>Save Changes
                                    </button>
                                    <button
                                        type="button"
                                        class="btn btn-danger"
                                        @click="deleteTransaction(currentTransaction.id)"
                                    >
                                        <i class="fas fa-trash mr-2"></i>Delete
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import TransactionCard from '@/components/TransactionCard.vue';

export default {
    components: {
        TransactionCard,
    },
    data() {
        return {
            transactions: [],
            categories: ['Makan', 'Jajan', 'Belanja', 'Hiburan', 'Transport'],
            dateRangeStart: null,
            dateRangeEnd: null,
            selectedCategories: [],
            showEditModal: false,
            currentTransaction: {},
            budgetByCategory: {
                Makan: 100000,
                Jajan: 200000,
                Belanja: 300000,
                Hiburan: 400000,
                Transport: 500000,
            },
        };
    },
    computed: {
        filteredTransactions() {
            const grouped = {};
            this.transactions.filter((transaction) => {
                const isWithinDateRange =
                    (!this.dateRangeStart ||
                        transaction.date >= this.dateRangeStart) &&
                    (!this.dateRangeEnd ||
                        transaction.date <= this.dateRangeEnd);
                const isSelectedCategory =
                    this.selectedCategories.length === 0 ||
                    this.selectedCategories.includes(transaction.category);
                return isWithinDateRange && isSelectedCategory;
            }).forEach((transaction) => {
                const dateKey = transaction.date;
                if (!grouped[dateKey]) {
                    grouped[dateKey] = {};
                }
                if (!grouped[dateKey][transaction.category]) {
                    grouped[dateKey][transaction.category] = transaction;
                }
            });
            return Object.keys(grouped).map((dateKey) => ({
                date: dateKey,
                ...grouped[dateKey],
            }));
        },
    },
    created() {
        this.fetchTransactions();
        this.fetchBudgetLimits();
    },
    methods: {
        totalAmount(category) {
            return this.filteredTransactions
                .filter((transactionGroup) => transactionGroup[category])
                .map((transactionGroup) => transactionGroup[category].amount)
                .reduce((total, amount) => total + amount, 0);
        },
        fetchTransactions() {
            axios
                .get('http://127.0.0.1:5000/api/transactions')
                .then((response) => {
                    this.transactions = response.data.transactions;
                })
                .catch((error) => {
                    console.error('Error fetching transactions:', error);
                });
        },
        fetchBudgetLimits() {
            axios
                .get('http://127.0.0.1:5000/api/budget-limits')
                .then((response) => {
                    this.budgetByCategory = response.data.budgetLimits;
                })
                .catch((error) => {
                    console.error('Error fetching budget limits:', error);
                });
        },
        updateBudgetLimit(category) {
            axios
                .put('http://127.0.0.1:5000/api/budget-limits', {
                    category: category,
                    limit: this.budgetByCategory[category]
                })
                .then((response) => {
                    console.log('Budget limit updated successfully');
                })
                .catch((error) => {
                    console.error('Error updating budget limit:', error);
                });
        },
        navigateToTransactionForm(category) {
            this.$router.push({
                name: 'TransactionForm',
                params: { selectedCategory: category },
            });
        },
        deleteTransaction(transactionId) {
            axios
                .delete(
                    `http://127.0.0.1:5000/api/transactions/${transactionId}`
                )
                .then(() => {
                    this.transactions = this.transactions.filter(
                        (transaction) => transaction.id !== transactionId
                    );
                    this.closeEditModal();
                })
                .catch((error) => {
                    console.error('Error deleting transaction:', error);
                });
        },
        openEditModal(transaction) {
            this.currentTransaction = { ...transaction };
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
        },
        updateTransaction() {
            axios
                .put(
                    `http://127.0.0.1:5000/api/transactions/${this.currentTransaction.id}`,
                    this.currentTransaction
                )
                .then((response) => {
                    console.log(response.data);
                    this.showEditModal = false;
                    this.fetchTransactions();
                })
                .catch((error) => {
                    console.error('Error updating transaction:', error);
                });
        },
        logout() {
            this.$router.push('/');
        },
    },
};
</script>

<style scoped>
.money-tracker-container {
    background-color: #f4f6f9;
    min-height: 100vh;
}

.card {
    border-radius: 10px;
}

.table-hover tbody tr:hover {
    background-color: rgba(0, 123, 255, 0.05);
}

.custom-control-input:checked + .custom-control-label::before {
    background-color: #007bff;
    border-color: #007bff;
}

.btn-outline-light {
    border-width: 2px;
}

.modal .modal-content {
    border-radius: 10px;
}

@media (max-width: 768px) {
    .input-group-prepend, .input-group-append {
        display: none;
    }
}
</style>