package cmd

import (
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"os"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
	"github.com/labstack/gommon/log"
	"path/filepath"
	"strings"
	"ModelHub-server/controllers"
)

var serverCmd = &cobra.Command{
	Use:"server",
	Short:"start server",
	Long:"start server",
	Run: func(cmd *cobra.Command, args []string) {
		addr := viper.GetString("server.listenAddr")
		uploadDir := viper.GetString("storage.local.dir")

		if _, err := os.Stat(uploadDir); os.IsNotExist(err) {
			os.Mkdir(uploadDir, 0755)
		}

		e := echo.New()
		e.Debug = viper.GetBool("server.debug")
		//e.HTTPErrorHandler =

		initEchoLog(e)
		addMiddlewares(e)
		addRoutes(e)

		e.Logger.Info("server pid ", os.Getpid())
		e.Logger.Info("server listening on ", addr)
		e.Logger.Fatal(e.Start(addr))
	},
}

func initEchoLog(e *echo.Echo) {
	w, err := os.OpenFile(filepath.Join(viper.GetString("dir.data"), viper.GetString("log.echo.file")), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0640)
	if err != nil {
		panic(err)
	}
	e.Logger.SetOutput(w)

	var lvl log.Lvl
	switch strings.ToUpper(viper.GetString("log.level")) {
	case "DEBUG":
		lvl = log.DEBUG
	case "INFO":
		lvl = log.INFO
	case "WARN":
		lvl = log.WARN
	case "ERROR":
		lvl = log.ERROR
	case "OFF":
		lvl = log.OFF
	default:
		lvl = log.INFO
	}
	e.Logger.SetLevel(lvl)
}

func addMiddlewares(e *echo.Echo) {
	e.Pre(middleware.RemoveTrailingSlash())

	e.Use(middleware.Recover())

	lcfg := middleware.DefaultLoggerConfig
	w, err := os.OpenFile(filepath.Join(viper.GetString("dir.data"), viper.GetString("log.request.file")), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0640)
	if err != nil {
		panic(err)
	}
	lcfg.Output = w
	e.Use(middleware.LoggerWithConfig(lcfg))

	e.Use(middleware.BasicAuth(func(username string, password string, c echo.Context) (bool, error) {
		if username == "yzs" && password == "12345" {
			return true, nil
		}
		return false, nil
	}))

	//e.Use(middlewares.Session())

	//e.Use(middlewares.MiddlewareContext())
}

func addRoutes(e *echo.Echo) {
	//auth := middlewares.Auth()

	e.POST("/register", controllers.RegisterAccount)
	e.GET("/login", controllers.Login)
	e.GET("/isLogined", controllers.IsLogined)
	e.GET("/logout", controllers.Logout)



	e.POST("/edit", controllers.EditAccount)
	e.GET("/info", controllers.AccountInfo)

}