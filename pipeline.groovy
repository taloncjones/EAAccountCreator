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
                    ssh josh@10.10.12.8 python3  /home/josh/dockerconfigs/jenkins/workspace/eaaccountcreator/main.py 'chrome' '/home/josh/dockerconfigs/jenkins/chromedriver' '/home/josh/dockerconfigs/jenkins/workspace/eaaccountcreator/accounts.json' \$eaaccountcreatorsheet '/home/josh/dockerconfigs/jenkins/workspace/eaaccountcreator/email.json'
                """
            }
          }
      }
   }
}
