<template>
    <el-scrollbar>
        <el-table :data="tableData">
            <el-table-column prop="date" label="Date" width="140" />
            <el-table-column prop="name" label="Name" width="120" />
            <el-table-column prop="address" label="Address" />
        </el-table>
    </el-scrollbar>
</template>

<script setup>
</script>