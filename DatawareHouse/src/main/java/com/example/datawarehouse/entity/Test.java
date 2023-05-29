package com.example.datawarehouse.entity;

public class Test {
    Integer id;
    String test;

    public Test() {
    }

    public Test(Integer id, String test) {
        this.id = id;
        this.test = test;
    }

    /**
     * 获取
     * @return id
     */
    public Integer getId() {
        return id;
    }

    /**
     * 设置
     * @param id
     */
    public void setId(Integer id) {
        this.id = id;
    }

    /**
     * 获取
     * @return test
     */
    public String getTest() {
        return test;
    }

    /**
     * 设置
     * @param test
     */
    public void setTest(String test) {
        this.test = test;
    }

    public String toString() {
        return "Test{id = " + id + ", test = " + test + "}";
    }
}
