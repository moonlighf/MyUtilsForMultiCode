# 介绍与使用方法
这个主要介绍了在Go中使用`Viper`模块进行配置参数的处理的方法

> Viper是适用于Go应用程序的完整配置解决方案。它被设计用于在应用程序中工作，并且可以处理所有类型的配置需求和格式。鉴于`viper`库本身的README已经写得十分详细。

### 01. 安装

```
go get github.com/spf13/viper
```

### 02. 读取配置文件

```go
viper.SetConfigFile("./config.yaml") // 指定配置文件路径
viper.SetConfigName("config") // 配置文件名称(无扩展名)
viper.SetConfigType("yaml") // 如果配置文件的名称中没有扩展名，则需要配置此项
viper.AddConfigPath("/etc/appname/")   // 查找配置文件所在的路径
viper.AddConfigPath("$HOME/.appname")  // 多次调用以添加多个搜索路径
viper.AddConfigPath(".")               // 还可以在工作目录中查找配置
err := viper.ReadInConfig() // 查找并读取配置文件
if err != nil { // 处理读取配置文件的错误
	panic(fmt.Errorf("Fatal error config file: %s n", err))
}
```

### 03. 读取配置文件值

在Viper中，有几种方法可以根据值的类型获取值。存在以下功能和方法:

- Get(key string) : interface{}

- GetBool(key string) : bool

- GetFloat64(key string) : float64

- GetInt(key string) : int

- GetIntSlice(key string) : []int

- GetString(key string) : string

- GetStringMap(key string) : map[string]interface{}

- GetStringMapString(key string) : map[string]string

- GetStringSlice(key string) : []string

- GetTime(key string) : time.Time

- GetDuration(key string) : time.Duration

- IsSet(key string) : bool

- AllSettings() : map[string]interface{} 

**需要认识到的一件重要事情是，每一个Get方法在找不到值的时候都会返回零值。为了检查给定的键是否存在，提供了`IsSet()`方法。**

```go
viper.GetString("logfile") // 不区分大小写的设置和获取
if viper.GetBool("verbose") {
    fmt.Println("verbose enabled")
}
```

### 04. 文件demo

- `readconfigcommon`：直接使用viper管理配置
- `readconfigstruct`：使用结构体变量保存配置信息

