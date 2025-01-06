package logger

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"gopkg.in/natefinch/lumberjack.v2"
	"os"
	"path/filepath"
)

var Logger *zap.Logger

// Init 初始化日志
func Init(logDir string) error {
	// 确保日志目录存在
	if err := os.MkdirAll(logDir, os.ModePerm); err != nil {
		return err
	}

	// 日志文件路径
	logFile := filepath.Join(logDir, "app.log")

	// 配置 Lumberjack 日志轮转
	lumberjackLogger := &lumberjack.Logger{
		Filename:   logFile, // 日志文件路径
		MaxSize:    100,     // 每个日志文件的最大大小（MB）
		MaxBackups: 30,      // 保留旧日志文件的最大数量
		MaxAge:     30,      // 保留旧日志文件的最大天数
		Compress:   true,    // 是否压缩旧日志文件
		LocalTime:  true,    // 使用本地时间
	}

	// 配置 Zap 的日志编码器
	encoderConfig := zapcore.EncoderConfig{
		TimeKey:        "time",
		LevelKey:       "level",
		NameKey:        "logger",
		CallerKey:      "caller",
		FunctionKey:    zapcore.OmitKey,
		MessageKey:     "msg",
		StacktraceKey:  "stacktrace",
		LineEnding:     zapcore.DefaultLineEnding,
		EncodeLevel:    zapcore.LowercaseColorLevelEncoder, // 带颜色的日志级别
		EncodeTime:     zapcore.ISO8601TimeEncoder,         // ISO8601 时间格式
		EncodeDuration: zapcore.StringDurationEncoder,      // 持续时间
		EncodeCaller:   zapcore.ShortCallerEncoder,         // 短路径调用者信息
	}

	// 设置日志级别
	atomicLevel := zap.NewAtomicLevel()
	atomicLevel.SetLevel(zap.InfoLevel) // 默认日志级别为 Info

	// 创建 Zap 核心
	core := zapcore.NewCore(
		zapcore.NewJSONEncoder(encoderConfig), // JSON 编码器
		zapcore.NewMultiWriteSyncer( // 多路输出
			zapcore.AddSync(lumberjackLogger), // 输出到文件
			zapcore.AddSync(os.Stdout),        // 输出到控制台
		),
		atomicLevel, // 日志级别
	)

	// 创建 Logger
	Logger = zap.New(core, zap.AddCaller(), zap.AddStacktrace(zapcore.ErrorLevel))

	// 替换全局 Logger
	zap.ReplaceGlobals(Logger)

	return nil
}

// Sync 刷新日志缓冲区
func Sync() {
	_ = Logger.Sync()
}
