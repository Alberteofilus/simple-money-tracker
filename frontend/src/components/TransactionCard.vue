<template>
    <div class="transaction-card" @dblclick="editTransaction">
        <p>{{ transaction.amount }} IDR</p>
        <p>{{ transaction.date }}</p>
        <p>{{ transaction.category }}</p>
        <p>{{ transaction.description }}</p>
    </div>
</template>

<script>
export default {
    props: ['transaction'],
    methods: {
        editTransaction() {
            this.$emit('edit-transaction', this.transaction);
        },
    },
};
</script>

<style scoped>
.transaction-card {
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    cursor: pointer;
    background-color: white;
}
</style>
