pipeline {
    agent any

    stages {
  
        stage('GetCode') {
   
            steps {
                git branch: 'feature_fix_coverage', url: 'https://github.com/wien996/CP1.B.DevopsCloudUnir.git'
            }
        }

        stage('Unit') {
   
            steps {
	
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
	 
                    bat '''
                        SET PYTHONPATH=%WORKSPACE%
                        C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pytest --junitxml=result-unit.xml test\\unit
                    '''
                    junit 'result*.xml'
                }
            }
        }	

        stage('Coverage') {
   
            steps {
	
                bat '''
                    SET PYTHONPATH=%WORKSPACE%
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\coverage xml
                '''
																			
	 
                cobertura coberturaReportFile: 'coverage.xml', 
                    lineCoverageTargets: '100,100,0', // Líneas: 100% obligatorio
                    conditionalCoverageTargets: '100,100,0' // Condiciones: 100% obligatorio
				 
            }
        }

        stage('Static Analysis: flake8') {
   
            steps {
	
                bat '''
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\flake8 --exit-zero --format=pylint app >flake8.out
                '''
                recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], 
                    qualityGates: [
                        [threshold: 8, type: 'TOTAL', unstable: true],
                        [threshold: 10, type: 'TOTAL', unstable: false]
                    ]
            }
        }

        stage('Security Analysis: Bandit') {
   
            steps {
	
                bat '''
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\bandit --exit-zero -r . -f custom -o bandit.out --msg-template  "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], 
                    qualityGates: [
                        [threshold: 2, type: 'TOTAL', unstable: true],
                        [threshold: 4, type: 'TOTAL', unstable: false]
                    ]
            }
        }
        
        stage('Performance: JMeter') {
   
            steps {
	
                bat '''
                    C:\\Users\\danie\\AppData\\Local\\Programs\\apache-jmeter-5.6.3\\bin\\jmeter -n -t test\\jmeter\\flask.jmx -f -l flask.jtl
                '''
                perfReport sourceDataFiles: 'flask.jtl'
            }
        }
    }
}
