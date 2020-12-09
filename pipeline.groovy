pipeline {
   agent any

   stages {
      stage('Setup configuration files') {
         steps {
            withCredentials([file(credentialsId: 'eaaccountcreatoremail', variable: 'eaaccountcreatoremail'),
                            file(credentialsId: 'eaaccountcreatoraccounts', variable: 'eaaccountcreatoraccounts'),
                            string(credentialsId: 'eaaccountcreatorsheet', variable: 'eaaccountcreatorsheet')]) {
                sh "cp \$eaaccountcreatoremail email.json"
                sh "cp \$eaaccountcreatoraccounts accounts.json"
                sh "chmod 777 email.json"
                sh "chmod 777 accounts.json"
                sh "cat accounts.json"
            }
         }
      }
      stage('Run EAAccountCreator script') {
          steps {
              withCredentials([string(credentialsId: 'eaaccountcreatorsheet', variable: 'eaaccountcreatorsheet')]) {
                sh """
                	pip3 install -r requirements.txt
                    python3 main.py 'chrome' '/var/lib/jenkins/workspace/eaaccountcreator/chromedriver' 'accounts.json' \$eaaccountcreatorsheet 'email.json'
                """
            }
          }
      }
   }
}
