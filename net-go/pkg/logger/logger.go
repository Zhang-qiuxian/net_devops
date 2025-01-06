package logger

import (
	"os"
	"path/filepath"
	"sync"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"gopkg.in/natefinch/lumberjack.v2"
)

var (
	RequestLogger *zap.Logger
	ErrorLogger   *zap.Logger
	ApiLogger     *zap.Logger
	once          sync.Once
)

// Init 初始化日志
func Init(logDir string) error {
	var initError error
	once.Do(func() {
		// 确保日志目录存在
		if err := os.MkdirAll(logDir, os.ModePerm); err != nil {
			initError = err
			return
		}

		// 配置日志编码器
		encoderConfig := zapcore.EncoderConfig{
			TimeKey:        "time",
			LevelKey:       "level",
			NameKey:        "logger",
			CallerKey:      "caller",
			FunctionKey:    zapcore.OmitKey,
			MessageKey:     "msg",
			StacktraceKey:  "stacktrace",
			LineEnding:     zapcore.DefaultLineEnding,
			EncodeLevel:    zapcore.LowercaseColorLevelEncoder,
			EncodeTime:     zapcore.ISO8601TimeEncoder,
			EncodeDuration: zapcore.StringDurationEncoder,
			EncodeCaller:   zapcore.ShortCallerEncoder,
		}

		// 初始化请求日志
		RequestLogger = createLogger(filepath.Join(logDir, "request.log"), encoderConfig, zap.InfoLevel)

		// 初始化错误日志
		ErrorLogger = createLogger(filepath.Join(logDir, "error.log"), encoderConfig, zap.ErrorLevel)

		// 初始化操作日志
		ApiLogger = createLogger(filepath.Join(logDir, "api.log"), encoderConfig, zap.InfoLevel)
	})

	return initError
}

// createLogger 创建一个新的 Logger
func createLogger(logFile string, encoderConfig zapcore.EncoderConfig, level zapcore.Level) *zap.Logger {
	// 配置 Lumberjack 日志轮转
	lumberjackLogger := &lumberjack.Logger{
		Filename:   logFile,
		MaxSize:    100, // 每个日志文件的最大大小（MB）
		MaxBackups: 30,  // 保留旧日志文件的最大数量
		MaxAge:     30,  // 保留旧日志文件的最大天数
		Compress:   true,
	}

	// 创建 Zap 核心
	core := zapcore.NewCore(
		zapcore.NewJSONEncoder(encoderConfig), // JSON 编码器
		zapcore.NewMultiWriteSyncer( // 多路输出
			zapcore.AddSync(lumberjackLogger), // 输出到文件
			zapcore.AddSync(os.Stdout),        // 输出到控制台
		),
		level, // 日志级别
	)

	// 创建 Logger
	return zap.New(core, zap.AddCaller(), zap.AddStacktrace(zapcore.ErrorLevel))
}

// Sync 刷新所有日志缓冲区
func Sync() {
	_ = RequestLogger.Sync()
	_ = ErrorLogger.Sync()
	_ = ApiLogger.Sync()
}
