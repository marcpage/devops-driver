Usage:

  settings [-h | --help] 
  settings --secrets
  settings <value>...

-h --help  Display this help information

--secrets  Prompt for any secrets that have not been set in the keychain
            For secrets that are set, confirms that the value is set

<value>    A value to display the value for. For instance:
                "smtp" will display all the smtp values (but not secrets in smtp, like password)
                "smtp.server" will display just the smtp server
